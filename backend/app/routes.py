from fastapi import APIRouter, HTTPException
import sqlite3
from datetime import datetime
from backend.app.models import StarterRequest, FactCheckRequest, FeedbackRequest, DB_FILE
from backend.app.services import fetch_wikipedia_summary, analyze_and_generate_starters

router = APIRouter()

@router.post("/generate-starters", tags=["Core Features"])
async def generate_starters(payload: StarterRequest):
    """
    Scenario 1: Logs event metrics, triggers Varshini's NLP starter generations, 
    and saves transactional information safely into SQLite rows.
    """
    try:
        # Execute Varshini's dynamic text analysis and prompt-generation engine
        generation_result = analyze_and_generate_starters(payload.event_description, payload.interests)
        
        # Flatten the dynamic starters list using specific delimiters for storage
        starters_str = "||".join(generation_result["starters"])
        
        # Database Insert Operation
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversation_history (event_description, interests, generated_starters, timestamp) VALUES (?, ?, ?, ?)",
            (payload.event_description, payload.interests, starters_str, datetime.now().isoformat())
        )
        conn.commit()
        session_id = cursor.lastrowid
        conn.close()

        return {
            "session_id": session_id,
            "extracted_themes": generation_result["extracted_themes"],
            "starters": generation_result["starters"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fact-check", tags=["Core Features"])
async def fact_check(payload: FactCheckRequest):
    """
    Scenario 2: Triggers quick live verification search pipelines via Wikipedia API.
    """
    try:
        verification_result = fetch_wikipedia_summary(payload.topic)
        return {
            "topic": payload.topic,
            "verified_summary": verification_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", tags=["History & Feedback"])
async def get_history():
    """
    Scenario 3: Exposes logged records back to the interface screens.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, event_description, interests, generated_starters, feedback, timestamp FROM conversation_history")
        rows = cursor.fetchall()
        conn.close()

        history_list = []
        for row in rows:
            history_list.append({
                "id": row[0],
                "event_description": row[1],
                "interests": row[2],
                "starters": row[3].split("||"),  # Deflate flat database items back to JSON arrays
                "feedback": row[4],
                "timestamp": row[5]
            })
        return {"history": history_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback", tags=["History & Feedback"])
async def submit_feedback(payload: FeedbackRequest):
    """
    Scenario 3: Records user thumbs up/down updates into session rows.
    """
    try:
        feedback_status = "thumbs_up" if payload.is_useful else "thumbs_down"
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE conversation_history SET feedback = ? WHERE id = ?",
            (feedback_status, payload.session_id)
        )
        conn.commit()
        conn.close()
        return {"status": "success", "message": f"Feedback updated to {feedback_status}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
