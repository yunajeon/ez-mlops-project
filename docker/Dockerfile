# syntax=docker/dockerfile:1.7
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     HF_HOME=/hf     TRANSFORMERS_CACHE=/hf/transformers     HUGGINGFACE_HUB_CACHE=/hf/hub     MODEL_DIR=/models/KR-FinBert-SC     MODEL_ID=snunlp/KR-FinBert-SC     SERVICE_NAME=sentiment-api     ENVIRONMENT=local     LOG_LEVEL=INFO     ENABLE_TRACING=true     OTEL_EXPORTER_OTLP_ENDPOINT=http://tempo:4317     SERVICE_VERSION=dev

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install torch CPU from official index (pin for reproducibility)
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
    torch==2.4.1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Download model at build time (reproducible image, easy rollback)
RUN python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='snunlp/KR-FinBert-SC', local_dir='/models/KR-FinBert-SC', local_dir_use_symlinks=False)" \
    && python -c "import os; print('Model files:', len(os.listdir('/models/KR-FinBert-SC')))"

COPY app /app/app

EXPOSE 8000

# Gunicorn with Uvicorn worker; default 1 worker for CPU model.
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "1", "-b", "0.0.0.0:8000", "app.main:app"]
