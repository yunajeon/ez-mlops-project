from prometheus_client import Counter, Histogram, Gauge

REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"]
)

REQUEST_LATENCY_SECONDS = Histogram(
    "http_request_latency_seconds",
    "HTTP request latency (seconds)",
    ["path"]
)

INFERENCE_LATENCY_SECONDS = Histogram(
    "model_inference_latency_seconds",
    "Model inference latency (seconds)"
)

MODEL_LOADED = Gauge(
    "model_loaded",
    "1 if model is loaded and ready, else 0"
)

PREDICTIONS_TOTAL = Counter(
    "predictions_total",
    "Total predictions made",
    ["label"]
)

ERRORS_TOTAL = Counter(
    "errors_total",
    "Total errors",
    ["type"]
)
