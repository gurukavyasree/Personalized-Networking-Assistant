from fastapi import APIRouter, HTTPException
import sqlite3
import json
from datetime import datetime
from backend.app.models import StarterRequest, FactCheckRequest, FeedbackRequest, DB_FILE
from backend.app.services import (
    fetch_wikipedia_summary, 
    analyze_and_generate_starters, 
    extract_event_themes, 
    generate_topics, 
    log_conversation,
    log_user_feedback
)

router = APIRouter()

@router.post("/analyze-event", tags=["Core API Tier"])
async def analyze_event(payload: StarterRequest):
    """
    Epic 2 Story 7: Standalone theme extraction capability.
    Useful for isolated validation testing or external custom API integrations.
    """
    try:
        themes = extract_event_themes(payload.event_description)
        return {"extracted_themes": themes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fact-check", tags=["Core API Tier"])
async def fact_check(payload: FactCheckRequest):
    """Wraps the external Wikipedia REST lookup module inside a type-safe contract."""
    try:
        result = fetch_wikipedia_summary(payload.topic)
        return {"topic": payload.topic, "verified_summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-conversation", tags=["Core API Tier"])
async def generate_conversation(payload: StarterRequest):
    """
    Primary orchestration endpoint. Extracts themes, builds prompt narratives, 
    and automatically executes side-effect persistence history tracking.
    """
    try:
        # 1. Trigger isolated zero-shot categorization theme extractor
        themes = extract_event_themes(payload.event_description)
        
        # 2. Feed extracted context models directly into generative text pipeline
        starters = generate_topics(themes, payload.interests)
        
        # 3. Automatic side-effect logging: records trace blocks onto disk without frontend triggers
        log_conversation(payload.event_description, payload.interests, themes, starters)
        
        # --- Relational Database Telemetry Fallback Storage Traces ---
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users_Profile (BioText, currentEventCache) VALUES (?, ?)", (payload.interests, payload.event_description))
        u_id = cursor.lastrowid
        cursor.execute("INSERT INTO Event_Context (EventDescription, AnalyzedThemes) VALUES (?, ?)", (payload.event_description, ", ".join(themes)))
        e_id = cursor.lastrowid
        cursor.execute("INSERT INTO Networking_Session (UserID, EventID, SessionTimestamp) VALUES (?, ?, ?)", (u_id, e_id, datetime.now().isoformat()))
        s_id = cursor.lastrowid
        for s in starters:
            cursor.execute("INSERT INTO Generated_Starter (SessionID, StarterText, ContextPromptUsed) VALUES (?, ?, ?)", (s_id, s, "GPT-2 pipeline context run"))
        conn.commit()
        conn.close()

        return {
            "session_id": s_id,
            "extracted_themes": themes,
            "starters": starters
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", tags=["History & Feedback"])
async def get_history():
    """Retrieves session transaction traces for structural dashboard rendering."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.SessionID, e.EventDescription, u.BioText, s.SessionTimestamp 
        FROM Networking_Session s
        JOIN Event_Context e ON s.EventID = e.EventID
        JOIN Users_Profile u ON s.UserID = u.UserID
    """)
    sessions = cursor.fetchall()
    history = []
    for s in sessions:
        cursor.execute("SELECT StarterText FROM Generated_Starter WHERE SessionID = ?", (s[0],))
        starters = [r[0] for r in cursor.fetchall()]
        history.append({
            "id": s[0], 
            "event_description": s[1], 
            "interests": s[2], 
            "starters": starters, 
            "timestamp": s[3]
        })
    conn.close()
    return {"history": history}

@router.post("/feedback", tags=["History & Feedback"])
async def submit_feedback(payload: FeedbackRequest):
    """Captures downstream user ratings to feed eventual prompt optimization tasks."""
    try:
        # Run secondary tracking telemetry
        log_user_feedback(f"Session Identifier Target: {payload.session_id}", payload.is_useful)
        return {"status": "success", "message": "Telemetry logged."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
