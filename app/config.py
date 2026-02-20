from pydantic import BaseModel
import os

class Settings(BaseModel):
    # Model
    model_id: str = os.getenv("MODEL_ID", "snunlp/KR-FinBert-SC")
    model_dir: str = os.getenv("MODEL_DIR", "/models/KR-FinBert-SC")
    max_length: int = int(os.getenv("MAX_LENGTH", "128"))
    batch_size: int = int(os.getenv("BATCH_SIZE", "8"))

    # API
    service_name: str = os.getenv("SERVICE_NAME", "sentiment-api")
    environment: str = os.getenv("ENVIRONMENT", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    request_timeout_ms: int = int(os.getenv("REQUEST_TIMEOUT_MS", "3000"))

    # Observability
    enable_tracing: bool = os.getenv("ENABLE_TRACING", "true").lower() == "true"
    otel_exporter_otlp_endpoint: str = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://tempo:4317")
    otel_service_version: str = os.getenv("SERVICE_VERSION", "dev")

settings = Settings()
