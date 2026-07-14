import requests

def analyze_and_generate_starters(event_description: str, interests: str) -> dict:
    """
    Scenario 1: Sai Varshini's Text Processing Pipeline.
    Dynamically extracts contextual key themes and generates personalized,
    targeted conversation starters based on the user's background.
    """
    # 1. Natural Language Processing (NLP) - Theme Extraction Simulation
    # Normalizes terms to simulate extracting categorical entities from user text
    combined_text = f"{event_description} {interests}".lower()
    
    extracted_themes = []
    theme_keywords = {
        "AI & Tech": ["ai", "artificial intelligence", "machine learning", "tech", "software", "data"],
        "Sustainability": ["sustainability", "green", "urban planning", "renewable", "environment"],
        "Career Development": ["career", "growth", "networking", "jobs", "management", "business"]
    }
    
    for theme, keywords in theme_keywords.items():
        if any(keyword in combined_text for keyword in keywords):
            extracted_themes.append(theme)
            
    # Default placeholder category fallback if no matching string tags found
    if not extracted_themes:
        extracted_themes = ["General Networking", "Professional Development"]

    # 2. Context-Aware Template Generation Engine
    # Synthesizes custom icebreaker structures mapping directly to inputs
    starters = [
        f"Hi! I noticed the agenda covers topics surrounding {extracted_themes[0]}. Given your interest in '{interests}', what are your thoughts on where the industry is heading?",
        f"Attending this '{event_description}' is quite exciting. I'm trying to connect with people focused on '{interests}'—how has your experience at the event been so far?"
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
