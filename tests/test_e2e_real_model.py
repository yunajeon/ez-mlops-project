import os
import pytest
from fastapi.testclient import TestClient

import app.main as mainmod

pytestmark = pytest.mark.e2e

def test_real_model_predict_smoke():
    # This test expects MODEL_DIR to exist or HF download available.
    # It may take time. Run explicitly: pytest -m e2e
    os.environ.setdefault("MODEL_ID", "snunlp/KR-FinBert-SC")
    # If you downloaded locally: export MODEL_DIR=./models/KR-FinBert-SC

    app = mainmod.create_app()
    client = TestClient(app)

    # Wait for startup load
    r = client.get("/readyz")
    if r.status_code != 200:
        pytest.skip("Model not loaded in this environment. Download the model and set MODEL_DIR, then rerun.")

    r = client.post("/v1/predict", json={"text":"실적이 개선되어 주가가 상승했다."})
    assert r.status_code == 200
    data = r.json()
    assert "predictions" in data
    assert len(data["predictions"]) == 1
