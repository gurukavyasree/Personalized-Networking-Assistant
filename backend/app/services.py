import requests

def fetch_wikipedia_summary(topic: str) -> str:
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
