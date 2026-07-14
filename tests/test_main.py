import os
import sqlite3
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models import DB_FILE

# Initialize the FastAPI TestClient
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Fixture to ensure a clean database state before and after tests."""
    # Setup: Ensure tables exist
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_description TEXT NOT NULL,
            interests TEXT NOT NULL,
            generated_starters TEXT NOT NULL,
            feedback TEXT DEFAULT 'none',
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    
    yield  # Run the actual test case here
    
    # Teardown: Clean up the test records (Optional: can delete DB if needed)
    if os.path.exists(DB_FILE):
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversation_history")
            conn.commit()
            conn.close()
        except Exception:
            pass

def test_root_endpoint():
    """Validates that the base API root path responds successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Networking Assistant API is running successfully!"}

def test_generate_starters_endpoint():
    """Tests the core starter generation pipeline and database storage assertion."""
    payload = {
        "event_description": "Tech Dev Summit 2026",
        "interests": "Machine Learning and Python programming"
    }
    response = client.post("/api/generate-starters", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "session_id" in data
    assert "extracted_themes" in data
    assert len(data["starters"]) > 0
    assert "AI & Tech" in data["extracted_themes"]

def test_fact_check_endpoint():
    """Validates external API proxy validation logic functionality."""
    payload = {"topic": "Python programming language"}
    response = client.post("/api/fact-check", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["topic"] == "Python programming language"
    assert "verified_summary" in data

def test_get_history_endpoint():
    """Verifies that the database logs are fetched properly by the GET request."""
    # Generate an entry first to seed database records
    client.post("/api/generate-starters", json={
        "event_description": "History Test Event",
        "interests": "Data Analytics"
    })
    
    response = client.get("/api/history")
    assert response.status_code == 200
    
    data = response.json()
    assert "history" in data
    assert len(data["history"]) > 0

def test_submit_feedback_endpoint():
    """Validates relational entry updating features across SQLite logs."""
    # Seed a entry row to get a valid live session ID
    seed_res = client.post("/api/generate-starters", json={
        "event_description": "Feedback Test Event",
        "interests": "Testing Pipelines"
    })
    session_id = seed_res.json()["session_id"]
    
    # Send feedback payload update
    feedback_payload = {
        "session_id": session_id,
        "is_useful": True
    }
    response = client.post("/api/feedback", json=feedback_payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Feedback updated to thumbs_up"}
