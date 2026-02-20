import time
import uuid
import logging
from typing import Callable

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from .config import settings
from .logging_conf import setup_logging
from .schemas import PredictRequest, PredictResponse, Prediction, VersionResponse
from .model import ModelService
from .metrics import (
    REQUESTS_TOTAL, REQUEST_LATENCY_SECONDS, INFERENCE_LATENCY_SECONDS,
    MODEL_LOADED, PREDICTIONS_TOTAL, ERRORS_TOTAL
)
from .otel import setup_tracing

logger = logging.getLogger(__name__)
model_service = ModelService()

def create_app() -> FastAPI:
    setup_logging(settings.log_level)

    app = FastAPI(
        title="Sentiment API",
        version=settings.otel_service_version
    )
    setup_tracing(app, model_version="local")

    @app.on_event("startup")
    def _startup() -> None:
        try:
            info = model_service.load()
            MODEL_LOADED.set(1)
            # setup_tracing(app, model_version=info.model_version)
        except Exception as e:
            MODEL_LOADED.set(0)
            ERRORS_TOTAL.labels(type="startup_model_load").inc()
            logger.exception("Failed to load model on startup")
            # Let app start but readiness will fail; Kubernetes will keep it out of service.

    @app.middleware("http")
    async def request_context_middleware(request: Request, call_next: Callable):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        start = time.time()

        # Attach to request.state for handlers/logging
        request.state.request_id = request_id

        try:
            response: Response = await call_next(request)
        except Exception as e:
            ERRORS_TOTAL.labels(type="unhandled").inc()
            logger.exception("Unhandled error", extra={"request_id": request_id})
            response = JSONResponse(status_code=500, content={"error": "internal_error", "request_id": request_id})

        elapsed = time.time() - start
        path = request.url.path

        REQUEST_LATENCY_SECONDS.labels(path=path).observe(elapsed)
        REQUESTS_TOTAL.labels(method=request.method, path=path, status=str(response.status_code)).inc()

        response.headers["x-request-id"] = request_id
        return response

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/readyz")
    def readyz():
        if MODEL_LOADED._value.get() != 1:
            raise HTTPException(status_code=503, detail="model_not_loaded")
        return {"status": "ready"}

    @app.get("/version", response_model=VersionResponse)
    def version():
        info = model_service.info
        return VersionResponse(
            service=settings.service_name,
            service_version=settings.otel_service_version,
            model_id=settings.model_id,
            model_version=info.model_version if info else "unknown",
            environment=settings.environment,
        )

    @app.get("/metrics")
    def metrics():
        data = generate_latest()
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)

    @app.post("/v1/predict", response_model=PredictResponse)
    def predict(req: PredictRequest, request: Request):
        texts = req.normalized_texts()
        if not texts:
            raise HTTPException(status_code=400, detail="Provide 'text' or 'texts'")

        if MODEL_LOADED._value.get() != 1:
            raise HTTPException(status_code=503, detail="model_not_loaded")

        if len(texts) > 64:
            raise HTTPException(status_code=413, detail="Too many texts in one request (max=64)")

        t0 = time.time()
        try:
            preds_raw = model_service.predict(texts, return_all_scores=req.return_all_scores)
        except Exception:
            ERRORS_TOTAL.labels(type="inference").inc()
            logger.exception("Inference failed", extra={"request_id": getattr(request.state, "request_id", None)})
            raise HTTPException(status_code=500, detail="inference_failed")

        INFERENCE_LATENCY_SECONDS.observe(time.time() - t0)

        predictions = []
        for text, top_label, top_score, scores in preds_raw:
            PREDICTIONS_TOTAL.labels(label=top_label).inc()
            predictions.append(Prediction(text=text, top_label=top_label, top_score=top_score, scores=scores))

        info = model_service.info
        return PredictResponse(
            model_id=settings.model_id,
            model_version=info.model_version if info else "unknown",
            predictions=predictions
        )

    return app

app = create_app()
