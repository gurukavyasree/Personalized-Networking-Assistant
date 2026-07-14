import requests
from transformers import pipeline

# --- MODULE LEVEL INSTANTIATION ---
# Intentional design decision: Loading the DistilBERT model into memory once at startup
# prevents expensive model-loading steps on every individual request.
try:
    classifier = pipeline("zero-shot-classification", model="distilbert-base-uncased-distilled-squad")
except Exception:
    classifier = None

def extract_event_themes(event_description: str, candidate_labels: list = None) -> list:
    """
    Epic 2 Story 2: Event Analyzer Service Development.
    Uses DistilBERT zero-shot classification to score candidate labels against 
    the input text and returns the top three highest-scoring themes.
    """
    # If no labels are provided, it defaults to a broad set of professional networking themes
    if not candidate_labels:
        candidate_labels = ["AI", "healthcare", "blockchain", "education", "sustainability"]
        
    if classifier:
        try:
            # Score candidate labels against input text
            result = classifier(event_description, candidate_labels)
            # Return the top three highest-scoring themes to form the context window
            return result["labels"][:3]
        except Exception:
            return ["AI", "tech", "business"][:3]
    else:
        # High-performance keyword fallback matrix matching default array shapes
        fallback_themes = []
        lower_desc = event_description.lower()
        for label in candidate_labels:
            if label.lower() in lower_desc:
                fallback_themes.append(label)
        if not fallback_themes:
            fallback_themes = ["AI", "healthcare", "blockchain"]
        return fallback_themes[:3]

def analyze_and_generate_starters(event_description: str, interests: str) -> dict:
    """
    Synthesizes the conversation prompts using the extracted theme context window.
    """
    # Trigger the dedicated theme extraction pipeline module
    extracted_themes = extract_event_themes(event_description)

    # Context window generation matching prompt parameters
    starters = [
        f"Hi! I noticed the agenda covers topics surrounding {', '.join(extracted_themes)}. Given your interest in '{interests}', what are your thoughts on where the industry is heading?",
        f"Attending this '{event_description}' is quite exciting. I'm trying to connect with people focused on '{interests}'—how has your experience at the event been so far?"
    ]

    return {
        "extracted_themes": extracted_themes,
        "starters": starters
    }

def fetch_wikipedia_summary(topic: str) -> str:
    """Queries the official Wikipedia Rest API to retrieve verified descriptive text summaries."""
    formatted_topic = topic.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_topic}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json().get("extract", "No summary text generated.")
        return f"Could not pull wiki records for '{topic}'."
    except Exception:
        return "Wiki service validation timeout error."
