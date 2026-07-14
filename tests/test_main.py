import pytest
import re
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services import fetch_wikipedia_summary

client = TestClient(app)

# --- EPIC 5 STORY 5: API ROUTE INTEGRATION TESTS ---

def test_generate_conversation_happy_path_integration():
    """
    Validates a successful end-to-end request-response cycle.
    Verifies payload deserialization, service routing orchestration, and response structure.
    """
    payload = {
        "event_description": "Tech Innovation Expo focusing on Green Energy networks.",
        "interests": "Solar tracking technology, sustainable design"
    }
    response = client.post("/api/generate-conversation", json=payload)
    
    assert response.status_code == 200, "Valid requests should return a 200 OK status."
    
    data = response.json()
    assert "session_id" in data, "Response framework must contain a session identifier."
    assert "extracted_themes" in data, "Themes array must be included."
    assert "starters" in data, "Generated icebreaker array list must be returned."
    assert len(data["starters"]) == 3, "Exactly three icebreaker starters must be provided."

def test_invalid_request_returns_422():
    """
    Validates Pydantic serialization layer constraints.
    Verifies that sending an invalid/empty payload triggers an automatic 422 Unprocessable Entity
    error without needing manual error handling code.
    """
    # Empty JSON payload violates Pydantic models requiring 'event_description' and 'interests'
    invalid_payload = {}
    response = client.post("/api/generate-conversation", json=invalid_payload)
    
    assert response.status_code == 422, "Missing required schema fields must result in a 422 error code."
    
    error_detail = response.json()
    assert "detail" in error_detail, "Error responses must provide structured field exceptions."


# --- PREVIOUS SYSTEM MOCKED UNIT TESTS ---

@patch("backend.app.services.requests.get")
def test_fetch_wikipedia_summary_happy_path(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"extract": "Python is a high-level programming language."}
    mock_get.return_value = mock_response

    result = fetch_wikipedia_summary("Python")
    assert result == "Python is a high-level programming language."

def test_root_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
