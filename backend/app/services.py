import requests
import re
import json
from datetime import datetime
from pathlib import Path
from transformers import pipeline, set_seed

# Fix random seed for reproducibility
set_seed(42)

# --- EPIC 2 STORY 5: JSON HISTORY LOGGER MECHANISM ---
# Using pathlib.Path ensures cross-platform compatibility across Windows, macOS, and Linux
HISTORY_FILE = Path("conversation_history.json")

def load_history() -> list:
    """Provides a clean read interface that always returns a list, even when no history exists."""
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def log_conversation(event_description: str, interests: str, extracted_themes: list, starters: list):
    """
    Appends the conversation metrics using a read-modify-write pattern to ensure data integrity.
    Includes an ISO-formatted timestamp on every session block.
    """
    history_data = load_history()
    
    # Construct data record structure with ISO-formatted timestamp
    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_description": event_description,
        "interests": interests,
        "extracted_themes": extracted_themes,
        "starters": starters
    }
    
    # Simple append-to-JSON-list pattern
    history_data.append(new_entry)
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=4)


# --- TRANSFORMATION PIPELINES MODULE LOAD ---
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
    
    # Trigger the file-based JSON history logger append event
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
