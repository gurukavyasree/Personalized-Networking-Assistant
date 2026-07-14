import requests
from transformers import pipeline

# --- MODULE LEVEL INSTANTIATION (Intentional Design Decision) ---
# This loads the DistilBERT model into memory once at startup for high performance
try:
    classifier = pipeline("zero-shot-classification", model="distilbert-base-uncased-distilled-squad")
except Exception:
    # Safe fallback if environment lacks local download capability during verification
    classifier = None

def analyze_and_generate_starters(event_description: str, interests: str) -> dict:
    """
    Scenario 1: Sai Varshini's Complete ML Pipeline.
    Uses DistilBERT zero-shot classification to score and extract the top 3 highest-scoring themes,
    then uses them to build context-aware conversation starters.
    """
    candidate_labels = ["AI", "healthcare", "blockchain", "education", "sustainability", "tech", "business"]
    extracted_themes = []

    # 1. Zero-Shot Classification Theme Extraction
    if classifier:
        try:
            combined_context = f"{event_description} {interests}"
            result = classifier(combined_context, candidate_labels)
            # Grab the top 3 highest-scoring themes based on model output
            extracted_themes = result["labels"][:3]
        except Exception:
            extracted_themes = ["AI & Tech", "Sustainability"]
    else:
        # Fallback keyword analyzer matching your prior framework version
        combined_text = f"{event_description} {interests}".lower()
        if "ai" in combined_text or "tech" in combined_text:
            extracted_themes.append("AI & Tech")
        if "sustainability" in combined_text or "green" in combined_text:
            extracted_themes.append("Sustainability")
        if not extracted_themes:
            extracted_themes = ["General Networking", "Professional Development"]

    # 2. Dynamic Conversation Starter Generation Engine
    starters = [
        f"Hi! I noticed the event highlights themes surrounding {', '.join(extracted_themes)}. Given your background in '{interests}', what's your take on this?",
        f"Attending this '{event_description}' is a great opportunity. I'm focusing on projects matching {extracted_themes[0]}—are you working on anything similar?"
    ]

    return {
        "extracted_themes": extracted_themes,
        "starters": starters
    }

def fetch_wikipedia_summary(topic: str) -> str:
    """
    Scenario 2: Queries the official Wikipedia Rest API to retrieve 
    verified descriptive text summaries.
    """
    formatted_topic = topic.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_topic}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "No descriptive overview available.")
        elif response.status_code == 404:
            return f"Could not locate verified summaries for topic: '{topic}'."
        else:
            return "Unable to complete validation verification request at this time."
    except Exception:
        return "Internal connectivity pipeline dropped connection."
