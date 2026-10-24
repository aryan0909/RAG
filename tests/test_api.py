
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "LanceDB RAG is Running!!"
    }


def test_search_rejects_empty_question():
    response = client.post(
        "/search",
        json={"question": "", "limit": 2},
    )

    assert response.status_code == 422


def test_search_rejects_invalid_limit():
    response = client.post(
        "/search",
        json={"question": "What is the leave policy?", "limit": 0},
    )

    assert response.status_code == 422


def test_search_returns_relevant_document():
    response = client.post(
        "/search",
        json={
            "question": "How many annual leave days can employees carry forward?",
            "limit": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["question"] == (
        "How many annual leave days can employees carry forward?"
    )
    assert len(data["results"]) == 2

    # The top result should contain the supporting policy.
    assert data["results"][0]["chunk_id"] == 0
    assert "maximum of 5 unused annual leave days" in (
        data["results"][0]["text"]
    )
