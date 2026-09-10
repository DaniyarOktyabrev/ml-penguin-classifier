import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")


def test_health():
    response = requests.get(f"{API_URL}/health", timeout=10)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_valid():
    payload = {
        "island": "Torgersen",
        "bill_length_mm": 39.1,
        "bill_depth_mm": 18.7,
        "flipper_length_mm": 181.0,
        "body_mass_g": 3750.0,
        "sex": "MALE"
    }
    response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert "species" in data
    assert data["species"] in ["Adelie", "Gentoo", "Chinstrap"]


def test_predict_invalid():
    payload = {"island": "Torgersen"}
    response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
    assert response.status_code == 422