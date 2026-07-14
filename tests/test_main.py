import pytest
import re
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services import extract_event_themes, generate_topics

client = TestClient(app)

def test_extract_event_themes_structural_contract():
    """Epic 5 Story 2: Event Analyzer Unit Tests."""
    candidate_labels = ["AI", "healthcare", "blockchain", "education", "sustainability"]
    sample_description = "A global summit discussing renewable energy, micro-grids, and carbon tracking."
    themes = extract_event_themes(sample_description, candidate_labels=candidate_labels)
    assert isinstance(themes, list)
    assert len(themes) <= 3
    assert len(themes) > 0
    for theme in themes:
        assert theme in candidate_labels

def test_topic_generator_post_processing_contract():
    """
    Epic 5 Story 3: Topic Generator Unit Tests.
    Validates that the text processing engine cleanly removes markdown symbols,
    leading digits, and bullet elements, producing only clean, non-empty conversation starter strings.
    """
    mock_themes = ["AI", "sustainability"]
    mock_interests = "deep learning neural networks"
    
    # Execute the topic generation block logic
    starters = generate_topics(mock_themes, mock_interests)
    
    # 1. Structural Container Check
    assert isinstance(starters, list), "Output must return a sequence list."
    assert len(starters) == 3, "Pipeline must consistently generate exactly 3 alternative starter variations."
    
    # 2. String Hygiene & Non-Empty Validations
    for line in starters:
        assert isinstance(line, str), "Each starter item must be a valid string text entity."
        
        # Test that post-processing didn't result in an empty string (which creates blank UI bubbles)
        assert len(line.strip()) > 10, "Post-processed string must contain actual dialogue content, not empty rows."
        
        # Test that raw text bullet markers ('1.', '-', '*') are successfully stripped away
        assert not line.startswith("1."), "Post-processing pipeline must strip text generator index numbering prefixes."
        assert not line.startswith("-"), "Post-processing logic must clean raw hyphens and markdown points."
        assert not re.match(r'^\d+\.', line), "Cleaned lines must not retain leading numerical sequencing prefixes."

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
