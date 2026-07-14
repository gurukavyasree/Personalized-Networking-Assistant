from fastapi import APIRouter, HTTPException
import sqlite3
from datetime import datetime
from backend.app.models import StarterRequest, FactCheckRequest, FeedbackRequest, DB_FILE
from backend.app.services import fetch_wikipedia_summary

router = APIRouter()

@router.post("/generate-starters", tags=["Core Features"])
async def generate_starters(payload: StarterRequest):
    try:
        mock_starters = [
            f"I see you're interested in {payload.interests}. How do you see AI shaping this space?",
            f"Based on the event theme, what's your biggest takeaway regarding urban planning?"
        ]
        starters_str = "||".join(mock_starters)
        
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
            "extracted_themes": ["AI", "Sustainability"],
            "starters": mock_starters
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fact-check", tags=["Core Features"])
async def fact_check(payload: FactCheckRequest):
    try:
        verification_result = fetch_wikipedia_summary(payload.topic)
        return {"topic": payload.topic, "verified_summary": verification_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", tags=["History & Feedback"])
async def get_history():
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
                "starters": row[3].split("||"),
                "feedback": row[4],
                "timestamp": row[5]
            })
        return {"history": history_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback", tags=["History & Feedback"])
async def submit_feedback(payload: FeedbackRequest):
    try:
        feedback_status = "thumbs_up" if payload.is_useful else "thumbs_down"
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE conversation_history SET feedback = ? WHERE id = ?", (feedback_status, payload.session_id))
        conn.commit()
        conn.close()
        return {"status": "success", "message": f"Feedback updated to {feedback_status}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
