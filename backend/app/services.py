import requests
import re
import json
from datetime import datetime
from pathlib import Path
from transformers import pipeline, set_seed

# Fix random seed for reproducibility
set_seed(42)

# --- TRACKING PATH REGISTRY ---
HISTORY_FILE = Path("conversation_history.json")
FEEDBACK_FILE = Path("user_feedback.json")  # Pathlib handling for explicit user feedback logs

# --- EPIC 2 STORY 5: JSON HISTORY LOGGER ---
def load_history() -> list:
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def log_conversation(event_description: str, interests: str, extracted_themes: list, starters: list):
    history_data = load_history()
    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_description": event_description,
        "interests": interests,
        "extracted_themes": extracted_themes,
        "starters": starters
    }
    history_data.append(new_entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=4)


# --- EPIC 2 STORY 6: JSON FEEDBACK LOGGER MECHANISM ---
def load_feedback_records() -> list:
    """Helper to ensure clean array read access interfaces."""
    if not FEEDBACK_FILE.exists():
        return []
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def log_user_feedback(suggestion_text: str, is_useful: bool):
    """
    Epic 2 Story 6: Feedback Logger Service Development.
    Captures the exact suggestion text, maps usability to 'like' or 'dislike' strings,
    and appends records with a precise timestamp using a cross-platform Path tracker.
    """
    feedback_data = load_feedback_records()
    
    # Structural mapping to 'like' or 'dislike' action strings
    action_type = "like" if is_useful else "dislike"
    
    new_feedback = {
        "suggestion_text": suggestion_text,
        "action": action_type,
        "timestamp": datetime.now().isoformat()
    }
    
    feedback_data.append(new_feedback)
    
    # Write entire updated array list structurally back onto the local disk platform
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedback_data, f, indent=4)


# --- MACHINE LEARNING MODEL INFERENCE ENGINE MODULE ---
try:
    classifier = pipeline("zero-shot-classification", model="distilbert-base-uncased-distilled-squad")
    generator = pipeline("text-generation", model="gpt2")
except Exception:
    classifier = None
    generator = None

def extract_event_themes(event_description: str, candidate_labels: list = None) -> list:
    if not candidate_labels:
        candidate_labels = ["AI", "healthcare", "blockchain", "education", "sustainability"]
    if classifier:
        try:
            result = classifier(event_description, candidate_labels)
            return result["labels"][:3]
        except Exception:
            return ["AI", "tech", "business"][:3]
    return ["AI", "healthcare", "blockchain"][:3]

def generate_topics(extracted_themes: list, interests: str) -> list:
    themes_str = ", ".join(extracted_themes)
    prompt = (
        f"I am attending a professional networking event focused on {themes_str}. "
        f"My professional background and core interests include: {interests}.\n"
        f"Here are three natural, short, engaging conversation starter lines I will use:\n1."
    )
    starters = []
    if generator:
        try:
            outputs = generator(prompt, max_length=80, num_return_sequences=1, do_sample=True, temperature=0.7)
            gen_text = outputs[0]["generated_text"].replace(prompt, "1.").strip()
            lines = gen_text.split("\n")
            for line in lines:
                cleaned = re.sub(r'^[\d\.\-\*\s]+', '', line).strip()
                if len(cleaned) > 10 and len(starters) < 3:
                    starters.append(cleaned)
        except Exception:
            pass

    if len(starters) < 2:
        starters = [
            f"Hi! I noticed this session highlights themes surrounding {themes_str}. Given your focus on '{interests}', what are your thoughts on where things are heading?",
            f"Great event so far! I'm trying to connect with professionals working with '{interests}'—how has your experience been?",
            f"What brings you to this track? I found the topics about {extracted_themes[0] if extracted_themes else 'tech'} closely align with my background."
        ]
    return starters[:3]

def analyze_and_generate_starters(event_description: str, interests: str) -> dict:
    themes = extract_event_themes(event_description)
    starters = generate_topics(themes, interests)
    log_conversation(event_description, interests, themes, starters)
    return {"extracted_themes": themes, "starters": starters}

def fetch_wikipedia_summary(topic: str) -> str:
    formatted_topic = topic.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_topic}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json().get("extract", "No summary text generated.")
        return f"Could not pull wiki records for '{topic}'."
    except Exception:
        return "Wiki service validation timeout error."
