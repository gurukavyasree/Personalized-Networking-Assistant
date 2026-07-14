import sys
from pathlib import Path

# --- DYNAMIC PYTHON PATH MANIPULATION ---
# Ensures the front-end presentation layer can resolve and import parent service tier packages
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import requests

# --- CONNECTION HOST CONSTANT REGISTRY ---
BASE_URL = "http://127.0.0.1:8080/api"

st.set_page_config(
    page_title="AI Personalized Networking Assistant",
    page_icon="🤝",
    layout="wide"
)

st.title("🤝 AI-Powered Personalized Networking Assistant")
st.caption("Enterprise UI Client supporting Zero-Shot Analysis and Generative NLP Workflows")

# --- EPIC 4 STORIES 5 & 6: CONVERSATION HISTORY & FEEDBACK PANEL ---
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

# --- CORE INTERACTION TABS ---
tab1, tab2 = st.tabs(["🚀 Conversation Starter Engine", "🔍 Wiki Fact Validator"])

# Epic 4 Story 2: Input Section and Main Generation Flow
with tab1:
    st.header("Contextual Conversation Prompt Synthesis")
    st.write("Enter your event metrics below to extract zero-shot themes and trigger text generators.")
    
    event_desc = st.text_input("Event Description Summary:", placeholder="e.g., Annual Tech Summit on Clean Energy and Sustainability")
    user_interests = st.text_area("Your Core Competencies & Interests (Comma separated):", placeholder="e.g., AI, blockchain, healthcare")
    
    if st.button("Synthesize Conversation Starters", type="primary"):
        if event_desc.strip() and user_interests.strip():
            with st.spinner("Executing NLP Pipeline Orchestration Steps..."):
                try:
                    # Epic 4 Story 2: Interest parsing cleaning logic matrix array
                    cleaned_interests = [i.strip() for i in user_interests.split(',')]
                    joined_interests = ", ".join(cleaned_interests)
                    
                    payload = {"event_description": event_desc, "interests": joined_interests}
                    res = requests.post(f"{BASE_URL}/generate-conversation", json=payload)
                    
                    if res.status_code == 200:
                        data = res.json()
                        st.success("Analysis Complete!")
                        
                        st.subheader("🎯 Discovered Event Themes:")
                        st.write(", ".join(data["extracted_themes"]))
                        
                        # Epic 4 Story 7: State Management Implementation
                        st.session_state["active_session_id"] = data["session_id"]
                        st.session_state["last_starters"] = data["starters"]
                        
                except Exception:
                    st.error("Connection drops detected along the backend processing network tier.")
        else:
            st.warning("Please supply valid text contents for both context forms.")

    # Epic 4 Story 3: Results Display and Interactive Feedback System
    if "active_session_id" in st.session_state:
        st.markdown("---")
        st.subheader("💡 Suggested Icebreaker Suggestions:")
        
        for idx, starter in enumerate(st.session_state["last_starters"]):
            st.info(starter)
            col1, col2 = st.columns([1, 10])
            
            # Interactive rating logging actions
            if col1.button(f"👍 Upvote Prompt {idx+1}", key=f"like_{idx}"):
                try:
                    feedback_payload = {"session_id": st.session_state["active_session_id"], "is_useful": True}
                    requests.post(f"{BASE_URL}/feedback", json=feedback_payload)
                    st.toast("Positive telemetry rating logged successfully!")
                except Exception:
                    pass
                    
            if col2.button(f"👎 Downvote Prompt {idx+1}", key=f"dislike_{idx}"):
                try:
                    feedback_payload = {"session_id": st.session_state["active_session_id"], "is_useful": False}
                    requests.post(f"{BASE_URL}/feedback", json=feedback_payload)
                    st.toast("Negative feedback recorded for model optimization runs.")

# Epic 4 Story 4: Fact-Checking Interface Section
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
