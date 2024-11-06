from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_query():
    response = client.get("/query/?query=test")
    assert response.status_code == 200
    assert "results" in response.json()
