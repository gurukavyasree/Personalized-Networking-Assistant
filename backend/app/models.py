import sqlite3
from pydantic import BaseModel

DB_FILE = "networking_assistant.db"

def init_db():
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

init_db()

class StarterRequest(BaseModel):
    event_description: str
    interests: str

class FactCheckRequest(BaseModel):
    topic: str

class FeedbackRequest(BaseModel):
    session_id: int
    is_useful: bool
