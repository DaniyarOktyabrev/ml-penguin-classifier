from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_valid():
    payload = {
        "island": "Torgersen",
        "bill_length_mm": 39.1,
        "bill_depth_mm": 18.7,
        "flipper_length_mm": 181.0,
        "body_mass_g": 3750.0,
        "sex": "MALE"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "species" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200