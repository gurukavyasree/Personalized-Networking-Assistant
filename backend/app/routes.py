from fastapi import APIRouter, HTTPException
import sqlite3
import json
from datetime import datetime
from backend.app.models import StarterRequest, FactCheckRequest, FeedbackRequest, DB_FILE
from backend.app.services import fetch_wikipedia_summary, analyze_and_generate_starters

router = APIRouter()

@router.post("/generate-starters", tags=["Core Features"])
async def generate_starters(payload: StarterRequest):
    try:
        # 1. Evaluate input context via ML pipeline
        generation_result = analyze_and_generate_starters(payload.event_description, payload.interests)
        themes_str = ", ".join(generation_result["extracted_themes"])
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # 2. Populate User Profile cache mapping description metrics
        cursor.execute(
            "INSERT INTO Users_Profile (BioText, currentEventCache) VALUES (?, ?)", 
            (payload.interests, payload.event_description)
        )
        user_id = cursor.lastrowid
        
        # 3. Populate Event Context entity tracking parsed targets
        cursor.execute(
            "INSERT INTO Event_Context (EventDescription, AnalyzedThemes) VALUES (?, ?)",
            (payload.event_description, themes_str)
        )
        event_id = cursor.lastrowid
        
        # 4. Generate Core Transaction Record mapping relationships
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO Networking_Session (UserID, EventID, SessionTimestamp) VALUES (?, ?, ?)",
            (user_id, event_id, timestamp)
        )
        session_id = cursor.lastrowid
        
        # 5. Insert individual generated starter instances (1 to Many relationship execution)
        for starter in generation_result["starters"]:
            cursor.execute(
                "INSERT INTO Generated_Starter (SessionID, StarterText, ContextPromptUsed) VALUES (?, ?, ?)",
                (session_id, starter, f"Event prompt context: {themes_str}")
            )
            
        # 6. Audit System Log Logging Execution
        log_payload = json.dumps({"user_interests": payload.interests, "themes_discovered": generation_result["extracted_themes"]})
        cursor.execute(
            "INSERT INTO Log_Entry (SessionID, ActionType, PayloadJSON, Timestamp) VALUES (?, ?, ?, ?)",
            (session_id, "GENERATION_TRANSACTION", log_payload, timestamp)
        )
        
        conn.commit()
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
    try:
        verification_result = fetch_wikipedia_summary(payload.topic)
        
        # Seed an optional tracking log item
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        if payload.session_id:
            cursor.execute(
                "INSERT INTO Wikipedia_Fact_Check (SessionID, VerifiedQueryText, VerificationStatus, WikipediaSourceURL) VALUES (?, ?, ?, ?)",
                (payload.session_id, payload.topic, "SUCCESS", f"https://en.wikipedia.org/wiki/{payload.topic.replace(' ', '_')}")
            )
            conn.commit()
        conn.close()
        
        return {"topic": payload.topic, "verified_summary": verification_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", tags=["History & Feedback"])
async def get_history():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Querying data across normalized tables via simple joins or session sweeps
        cursor.execute("""
            SELECT s.SessionID, e.EventDescription, u.BioText, s.SessionTimestamp 
            FROM Networking_Session s
            JOIN Event_Context e ON s.EventID = e.EventID
            JOIN Users_Profile u ON s.UserID = u.UserID
        """)
        sessions = cursor.fetchall()

        history_list = []
        for sess in sessions:
            sess_id = sess[0]
            # Fetch relational child prompts linked directly to this identifier block
            cursor.execute("SELECT StarterText FROM Generated_Starter WHERE SessionID = ?", (sess_id,))
            starters = [r[0] for r in cursor.fetchall()]
            
            history_list.append({
                "id": sess_id,
                "event_description": sess[1],
                "interests": sess[2],
                "starters": starters if starters else ["No prompts saved"],
                "feedback": "logged",
                "timestamp": sess[3]
            })
            
        conn.close()
        return {"history": history_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback", tags=["History & Feedback"])
async def submit_feedback(payload: FeedbackRequest):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        # Log the feedback update action event directly to the telemetry audit logging entity
        cursor.execute(
            "INSERT INTO Log_Entry (SessionID, ActionType, PayloadJSON, Timestamp) VALUES (?, ?, ?, ?)",
            (payload.session_id, "FEEDBACK_SUBMISSION", json.dumps({"is_useful": payload.is_useful}), datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Feedback logged dynamically inside telemetry system entries"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
