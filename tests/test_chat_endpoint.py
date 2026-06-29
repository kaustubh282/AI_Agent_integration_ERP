import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "ERP Agent API is running"


def test_chat_fees_collection_flow(fixed_today):
    response = client.post(
        "/chat",
        json={"message": "Show fee collection for class 8A this month"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["detected_intent"] == "fees_collection"
    assert body["parameters"]["class_name"] == "8A"
    assert body["parameters"]["date_range"] == "this_month"
    assert "Fees Collection Report" in body["reply"]
    assert "₹13000" in body["reply"]


def test_chat_rejects_empty_message():
    response = client.post("/chat", json={"message": "   "})

    assert response.status_code == 422


def test_chat_requires_api_key_when_configured():
    with patch.dict(os.environ, {"AGENT_API_KEY": "test-secret-key"}):
        unauthorized = client.post(
            "/chat",
            json={"message": "Show fees outstanding for class 8A"},
        )
        authorized = client.post(
            "/chat",
            json={"message": "Show fees outstanding for class 8A"},
            headers={"X-API-Key": "test-secret-key"},
        )

    assert unauthorized.status_code == 401
    assert authorized.status_code == 200


def test_chat_does_not_expose_internal_errors():
    with patch(
        "agents.tool_router.get_fees_collection",
        side_effect=RuntimeError("database password leaked"),
    ):
        response = client.post(
            "/chat",
            json={"message": "Show fee collection for class 8A"},
        )

    assert response.status_code == 500
    assert "password" not in response.json()["reply"]
    assert response.json()["error_type"] == "internal_error"
