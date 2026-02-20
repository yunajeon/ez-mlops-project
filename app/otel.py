import logging
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

from .config import settings

logger = logging.getLogger(__name__)

def setup_tracing(app, model_version: str) -> None:
    if not settings.enable_tracing:
        logger.info("Tracing disabled")
        return

    resource = Resource.create({
        "service.name": settings.service_name,
        "service.version": settings.otel_service_version,
        "deployment.environment": settings.environment,
        "ml.model_id": settings.model_id,
        "ml.model_version": model_version,
    })

    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint, insecure=True)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # instrument fastapi
    FastAPIInstrumentor.instrument_app(app)
    LoggingInstrumentor().instrument(set_logging_format=True)

    logger.info("Tracing enabled", extra={"otlp_endpoint": settings.otel_exporter_otlp_endpoint})
