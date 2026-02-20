import logging
from pythonjsonlogger import jsonlogger

def setup_logging(level: str = "INFO") -> None:
    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove existing handlers (important in uvicorn reload / tests)
    for h in list(logger.handlers):
        logger.removeHandler(h)

    handler = logging.StreamHandler()
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s"
    formatter = jsonlogger.JsonFormatter(fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Silence noisy loggers if needed
    logging.getLogger("uvicorn.access").setLevel(level)
