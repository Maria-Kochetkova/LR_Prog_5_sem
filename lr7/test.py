import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Создает тестовый клиент для FastAPI."""
    with TestClient(app) as client:
        yield client

def test_get_rates(client):
    """Тестирует получение."""
    response = client.get("/")
    assert response.status_code == 200



