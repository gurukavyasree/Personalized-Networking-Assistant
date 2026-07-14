import sys
from pathlib import Path

# --- DYNAMIC PYTHON PATH MANIPULATION ---
# Allows the frontend layer script to cleanly resolve and import parent service tier packages
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import requests

# --- CONNECTION HUB REGISTRY ---
# Modifying this target host address changes the routing point for cloud staging environments
BASE_URL = "http://127.0.0.1:8080/api"

st.set_page_config(
    page_title="AI Personalized Networking Assistant",
    page_icon="🤝",
    layout="wide"
)

st.title("🤝 AI-Powered Personalized Networking Assistant")
st.caption("Finetuned Modular Interface with Zero-Shot & Generative NLP Pipelines")

# --- EXPANDABLE SESSION LOGGING TELEMETRY VIEWERS (Sidebar Panel) ---
st.sidebar.header("📜 Saved Session History")
if st.sidebar.button("Refresh Telemetry Feeds", type="secondary"):
    try:
        res = requests.get(f"{BASE_URL}/history")
        if res.status_code == 200:
            history_records = res.json().get("history", [])
            if not history_records:
                st.sidebar.info("No transaction logs archived on local disk database stacks yet.")
            for item in reversed(history_records):
                with st.sidebar.expander(f"📌 Session {item['id']} - {item['event_description'][:15]}..."):
                    st.caption(f"Logged: {item['timestamp'][:16]}")
                    st.write(f"**Interests Profile:** {item['interests']}")
                    st.write("**Generated Icebreaker Output:**")
                    for s in item["starters"]:
                        st.write(f"- {s}")
    except Exception:
        st.sidebar.error("Could not communicate with Backend Orchestration Server.")

# --- CORE APP TABS INTERACTION SECTION ---
tab1, tab2 = st.tabs(["🚀 Conversation Starter Engine", "🔍 Wiki Fact Validator"])

with tab1:
    st.header("Contextual Conversation Prompt Synthesis")
    st.write("Enter your event metrics below to extract zero-shot themes and trigger text generators.")
    
    event_desc = st.text_input("Event Description Summary:", placeholder="e.g., Annual Tech Summit on Clean Energy and Sustainability")
    user_interests = st.text_area("Your Core Competencies & Interests:", placeholder="e.g., Software Architecture, Solar Grid Analytics, Deep Learning")
    
    if st.button("Synthesize Conversation Starters", type="primary"):
        if event_desc.strip() and user_interests.strip():
            with st.spinner("Executing NLP Pipeline Orchestration Steps..."):
                try:
                    payload = {"event_description": event_desc, "interests": user_interests}
                    res = requests.post(f"{BASE_URL}/generate-conversation", json=payload)
                    
                    if res.status_code == 200:
                        data = res.json()
                        st.success("Analysis Complete!")
                        
                        # Render parsed classifications
                        st.subheader("🎯 Discovered Event Themes:")
                        st.write(", ".join(data["extracted_themes"]))
                        
                        # Save session token into internal Streamlit state management systems
                        st.session_state["active_session_id"] = data["session_id"]
                        st.session_state["last_starters"] = data["starters"]
                        
                except Exception:
                    st.error("Connection drops detected along the backend processing network tier.")
        else:
            st.warning("Please supply valid text contents for both context forms.")

    # Render dynamic prompts and feedback trackers if an active session state exists
    if "active_session_id" in st.session_state:
        st.markdown("---")
        st.subheader("💡 Suggested Icebreaker Suggestions:")
        
        for idx, starter in enumerate(st.session_state["last_starters"]):
            st.info(starter)
            col1, col2 = st.columns([1, 10])
            
            # Explicit user feedback logging triggers
            if col1.button(f"👍 Upvote Prompt {idx+1}", key=f"like_{idx}"):
                try:
                    feedback_payload = {"session_id": st.session_state["active_session_id"], "is_useful": True}
                    requests.post(f"{BASE_URL}/feedback", json=feedback_payload)
                    st.toast("Positive rating captured inside system logs!")
                except Exception:
                    pass
                    
            if col2.button(f"👎 Downvote Prompt {idx+1}", key=f"dislike_{idx}"):
                try:
                    feedback_payload = {"session_id": st.session_state["active_session_id"], "is_useful": False}
                    requests.post(f"{BASE_URL}/feedback", json=feedback_payload)
                    st.toast("Negative rating logged for optimization runs.")

with tab2:
    st.header("Defensive Fact Verification Module")
    st.write("Query the unauthenticated Wikipedia API layer to verify concepts safely.")
    
    topic_query = st.text_input("Concept or Topic to Verify:", placeholder="e.g., Large Language Models")
    if st.button("Run Verification Query", type="secondary"):
        if topic_query.strip():
            with st.spinner("Extracting verified reference blocks..."):
                try:
                    res = requests.post(f"{BASE_URL}/fact-check", json={"topic": topic_query})
                    if res.status_code == 200:
                        st.success("Verification Complete!")
                        st.info(res.json().get("verified_summary"))
                except Exception:
                    st.error("Verification processing engine timeout error.")
