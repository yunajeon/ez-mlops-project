.PHONY: venv install run test e2e docker-build docker-run compose-up compose-down bench

venv:
	python -m venv .venv

install:
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install --index-url https://download.pytorch.org/whl/cpu torch==2.4.1
	. .venv/bin/activate && pip install -r requirements.txt

download-model:
	. .venv/bin/activate && python scripts/download_model.py --out ./models/KR-FinBert-SC

run:
	. .venv/bin/activate && MODEL_DIR=./models/KR-FinBert-SC uvicorn app.main:app --host 0.0.0.0 --port 8000

test:
	. .venv/bin/activate && pytest -q

e2e:
	. .venv/bin/activate && MODEL_DIR=./models/KR-FinBert-SC pytest -q -m e2e

docker-build:
	docker build -f docker/Dockerfile -t sentiment-api:local .

docker-run:
	docker run --rm -p 8000:8000 sentiment-api:local

compose-up:
	cd docker && docker compose up --build -d

compose-down:
	cd docker && docker compose down -v

bench:
	. .venv/bin/activate && python scripts/bench.py --url http://localhost:8000/v1/predict --concurrency 10 --requests 200 --batch-size 4
