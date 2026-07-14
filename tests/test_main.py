import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services import extract_event_themes

client = TestClient(app)

def test_extract_event_themes_structural_contract():
    """
    Epic 5 Story 2: Event Analyzer Unit Tests.
    Validates structural properties of the DistilBERT theme classifier function 
    to ensure the contract remains robust against future AI model weight updates.
    """
    candidate_labels = ["AI", "healthcare", "blockchain", "education", "sustainability"]
    sample_description = "A global summit discussing renewable energy, micro-grids, and carbon tracking."
    
    # Run the underlying service function directly
    themes = extract_event_themes(sample_description, candidate_labels=candidate_labels)
    
    # 1. Structural Check: Is the output a list container type?
    assert isinstance(themes, list), "Theme extraction output must be a Python list."
    
    # 2. Size Check: Does it contain at most three items?
    assert len(themes) <= 3, "Pipeline must filter down to a maximum of 3 top themes."
    
    # 3. Content Check: Does it return at least one result?
    assert len(themes) > 0, "Pipeline should return at least one theme for a valid description."
    
    # 4. Domain Check: Are all items drawn directly from the candidate labels set?
    for theme in themes:
        assert theme in candidate_labels, f"Extracted theme '{theme}' was not in the original candidate labels list."

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
    assert "extracted_themes" in response.json()
