def fetch_wikipedia_summary(topic: str) -> str:
    """
    Epic 2 Story 4: Fact Checker Service Development.
    Queries the Wikipedia REST API without authentication keys to retrieve structured summary metrics.
    Uses defensive programming via an explicit try-except block to gracefully catch timeouts or network drops.
    """
    # Defensive programming: clean text and parse into accurate URL structures
    formatted_topic = topic.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_topic}"
    
    try:
        # Pull transactional JSON data directly from the verified external knowledge base
        res = requests.get(url, timeout=5)
        
        if res.status_code == 200:
            # Safely capture the first paragraph text extract from the structured JSON body
            return res.json().get("extract", "No summary text generated.")
        elif res.status_code == 404:
            return f"Could not find matching Wikipedia records for '{topic}'."
        else:
            return "External validation server responded with an error."
            
    except requests.exceptions.Timeout:
        # Handle unpredictable network latency issues gracefully without throwing a system crash
        return "Fact verification query timed out. Please try again."
    except Exception:
        # Catch-all safe fallback string to maintain total backend production uptime
        return "Internal connectivity pipeline dropped connection to the external validation service."
