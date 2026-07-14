import pytest
import re
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services import fetch_wikipedia_summary

client = TestClient(app)

# --- EPIC 5 STORY 4: MOCKED EXTERNAL APIS FACT-CHECKER TESTS ---

@patch("backend.app.services.requests.get")
def test_fetch_wikipedia_summary_happy_path(mock_get):
    """1. Happy Path: Simulates a successful 200 OK response with a valid extract snippet."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"extract": "Python is a high-level programming language."}
    mock_get.return_value = mock_response

    result = fetch_wikipedia_summary("Python")
    assert result == "Python is a high-level programming language."
    mock_get.assert_called_once_with("https://en.wikipedia.org/api/rest_v1/page/summary/Python", timeout=5)

@patch("backend.app.services.requests.get")
def test_fetch_wikipedia_summary_missing_data(mock_get):
    """2. Missing Data Path: Simulates a successful response that does not contain an extract field."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}  # Empty payload contract
    mock_get.return_value = mock_response

    result = fetch_wikipedia_summary("UnknownTopic")
    assert result == "No summary text generated."

@patch("backend.app.services.requests.get")
def test_fetch_wikipedia_summary_error_path(mock_get):
    """3. Error Path: Simulates an external API service timeout error or non-200 failure status code."""
    mock_get.side_effect = Exception("Connection Timeout")

    result = fetch_wikipedia_summary("TimeoutTopic")
    assert "timeout error" in result or "Could not pull" in result


# --- PREVIOUS SYSTEM LAYER BASIC UNIT TESTS ---

def test_root_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze_event_endpoint():
    payload = {
        "event_description": "Tech summit focused on deep learning neural networks.",
        "interests": "AI"
    }
    response = client.post("/api/analyze-event", json=payload)
    assert response.status_code == 200
