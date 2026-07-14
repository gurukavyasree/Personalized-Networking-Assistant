import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

# Instantiating the in-process TestClient wrapper framework
client = TestClient(app)

def test_root_health_check():
    """Verifies that the root infrastructure infrastructure is reachable and responsive."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "message": "Networking Assistant API is running successfully!"
    }

def test_analyze_event_endpoint():
    """Validates the isolated type-safe zero-shot theme classification engine routing layer."""
    payload = {
        "event_description": "Tech summit focused on deep learning neural networks and green micro-grids.",
        "interests": "AI, sustainability"
    }
    response = client.post("/api/analyze-event", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "extracted_themes" in data
    assert isinstance(data["extracted_themes"], list)
    assert len(data["extracted_themes"]) <= 3

def test_fact_check_endpoint():
    """Validates the defensive Wikipedia query api structure contract matches."""
    payload = {
        "topic": "Python programming language"
    }
    response = client.post("/api/fact-check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "topic" in data
    assert "verified_summary" in data
    assert data["topic"] == "Python programming language"

def test_generate_conversation_pipeline():
    """
    Validates the integrated multi-tier generation route orchestration.
    Ensures that theme extraction, GPT text processing, and fallback triggers 
    return a fully unified execution block.
    """
    payload = {
        "event_description": "BioTech conference exploring modern clinical diagnostics.",
        "interests": "healthcare analytics"
    }
    response = client.post("/api/generate-conversation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "extracted_themes" in data
    assert "starters" in data
    assert isinstance(data["starters"], list)
    assert len(data["starters"]) == 3
