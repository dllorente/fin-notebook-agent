from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_app_exists():
    assert app is not None


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
