from fastapi.testclient import TestClient
import app.main as mainmod

class FakeModel:
    def __init__(self):
        self.info = type("Info", (), {"model_version":"fake", "model_id":"fake"})()

    def load(self):
        return self.info

    def predict(self, texts, return_all_scores=True):
        out = []
        for t in texts:
            out.append((t, "positive", 0.9, {"positive":0.9, "negative":0.1}))
        return out

def test_healthz_and_predict(monkeypatch):
    # Patch global model_service and mark loaded
    monkeypatch.setattr(mainmod, "model_service", FakeModel())
    mainmod.MODEL_LOADED.set(1)

    app = mainmod.create_app()
    client = TestClient(app)

    r = client.get("/healthz")
    assert r.status_code == 200

    r = client.get("/readyz")
    assert r.status_code == 200

    r = client.post("/v1/predict", json={"text":"테스트"})
    assert r.status_code == 200
    data = r.json()
    assert data["predictions"][0]["top_label"] == "positive"

def test_validation():
    app = mainmod.create_app()
    client = TestClient(app)
    r = client.post("/v1/predict", json={})
    assert r.status_code == 400
