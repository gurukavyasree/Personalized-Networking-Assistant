import sqlite3
from pydantic import BaseModel
from typing import Optional, List

DB_FILE = "networking_assistant.db"

def init_db():
    """Initializes the fully normalized 6-table relational database schema."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Enable foreign key support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. User Profile Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users_Profile (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            BioText TEXT NOT NULL,
            currentEventCache TEXT
        )
    """)

    # 2. Event Context Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Event_Context (
            EventID INTEGER PRIMARY KEY AUTOINCREMENT,
            EventDescription TEXT NOT NULL,
            AnalyzedThemes TEXT
        )
    """)

    # 3. Networking Session Table (Focal point linking User and Event)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Networking_Session (
            SessionID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            EventID INTEGER NOT NULL,
            SessionTimestamp TEXT NOT NULL,
            FOREIGN KEY (UserID) REFERENCES Users_Profile(UserID) ON DELETE CASCADE,
            FOREIGN KEY (EventID) REFERENCES Event_Context(EventID) ON DELETE CASCADE
        )
    """)

    # 4. Generated Starter Table (1 to Many from Session)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Generated_Starter (
            StarterID INTEGER PRIMARY KEY AUTOINCREMENT,
            SessionID INTEGER NOT NULL,
            StarterText TEXT NOT NULL,
            ContextPromptUsed TEXT,
            FOREIGN KEY (SessionID) REFERENCES Networking_Session(SessionID) ON DELETE CASCADE
        )
    """)

    # 5. Wikipedia Fact Check Table (1 to Many from Session)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Wikipedia_Fact_Check (
            FactCheckID INTEGER PRIMARY KEY AUTOINCREMENT,
            SessionID INTEGER NOT NULL,
            VerifiedQueryText TEXT NOT NULL,
            VerificationStatus TEXT NOT NULL,
            WikipediaSourceURL TEXT,
            FOREIGN KEY (SessionID) REFERENCES Networking_Session(SessionID) ON DELETE CASCADE
        )
    """)

    # 6. Log Entry Table (System auditing & analytics logs)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Log_Entry (
            LogID INTEGER PRIMARY KEY AUTOINCREMENT,
            SessionID INTEGER,
            ActionType TEXT NOT NULL,
            PayloadJSON TEXT NOT NULL,
            Timestamp TEXT NOT NULL,
            FOREIGN KEY (SessionID) REFERENCES Networking_Session(SessionID) ON DELETE SET NULL
        )
    """)

    conn.commit()
    conn.close()

# Execute schema setup automatically on module initialization
init_db()


# --- Pydantic Structural Validation Schemas for Application Input/Output ---
class UserProfileModel(BaseModel):
    bio_text: str
    current_event_cache: Optional[str] = None

class StarterRequest(BaseModel):
    user_id: Optional[int] = None  # Links back to profile
    event_description: str
    interests: str

class FactCheckRequest(BaseModel):
    session_id: Optional[int] = None
    topic: str

class FeedbackRequest(BaseModel):
    session_id: int
    is_useful: bool
