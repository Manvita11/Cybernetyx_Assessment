from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ingest():
    with open("sample.txt", "rb") as file:
        response = client.post("/ingest/", files={"file": file})
    assert response.status_code == 200
    assert response.json() == {"status": "Document ingested successfully"}
