import requests
from transformers import pipeline

# --- MODULE LEVEL INSTANTIATION ---
# Loading models into memory once at startup ensures fast real-time web application responses
try:
    # DistilBERT for zero-shot theme extraction
    classifier = pipeline("zero-shot-classification", model="distilbert-base-uncased-distilled-squad")
    # GPT-2 Small for contextually coherent conversation generation
    generator = pipeline("text-generation", model="gpt2")
except Exception:
    classifier = None
    generator = None

def analyze_and_generate_starters(event_description: str, interests: str) -> dict:
    """
    Uses DistilBERT for Zero-Shot classification and GPT-2 to synthesize
    natural, engaging professional conversation starters.
    """
    candidate_labels = ["AI", "healthcare", "blockchain", "education", "sustainability", "tech"]
    extracted_themes = []

    # 1. DistilBERT Zero-Shot Classification
    if classifier:
        try:
            combined_context = f"{event_description} {interests}"
            res = classifier(combined_context, candidate_labels)
            extracted_themes = res["labels"][:3]
        except Exception:
            extracted_themes = ["Tech", "Business"]
    else:
        extracted_themes = ["General Networking"]

    # 2. GPT-2 Small Conversation Generation
    prompt = f"Create a short professional networking icebreaker line for an event about {', '.join(extracted_themes)} given the background: {interests}."
    
    starters = []
    if generator:
        try:
            # Generate short, punchy opening lines efficiently using GPT-2
            gen_outputs = generator(prompt, max_new_tokens=30, num_return_sequences=2, do_sample=True, temperature=0.7)
            for out in gen_outputs:
                text = out["generated_text"].replace(prompt, "").strip()
                # Clean up formatting artifacting if any exist
                clean_text = text.split("\n")[0] if "\n" in text else text
                if len(clean_text) > 10:
                    starters.append(clean_text)
        except Exception:
            pass

    # Fallback to structural context-aware templates if generation pipeline hits resource limits
    if len(starters) < 2:
        starters = [
            f"Hi! I noticed the event highlights themes surrounding {', '.join(extracted_themes)}. Given your background in '{interests}', what's your take on this?",
            f"Attending this '{event_description}' is a great opportunity. I'm focusing on projects matching {extracted_themes[0]}—are you working on anything similar?"
        ]

    return {"extracted_themes": extracted_themes, "starters": starters[:2]}

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
