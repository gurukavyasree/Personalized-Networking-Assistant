import sys
from pathlib import Path

# --- DYNAMIC PYTHON PATH MANIPULATION ---
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import requests

# --- CONNECTION HUB REGISTRY ---
BASE_URL = "http://127.0.0.1:8080/api"

st.set_page_config(
    page_title="AI Personalized Networking Assistant",
    page_icon="🤝",
    layout="wide"
)

st.title("🤝 AI-Powered Personalized Networking Assistant")
st.caption("Finetuned Modular Interface with Zero-Shot & Generative NLP Pipelines")

# --- SIDEBAR TELEMETRY DASHBOARD PANEL ---
st.sidebar.header("📜 Saved Session History")
if st.sidebar.button("Refresh History Feeds", type="secondary"):
    try:
        res = requests.get(f"{BASE_URL}/history")
        if res.status_code == 200:
            history_records = res.json().get("history", [])
            if not history_records:
                st.sidebar.info("No transaction logs archived yet.")
            else:
                # Slices for the 5 most recent entries to prevent UI bloating
                recent_history = history_records[-5:]
                for item in reversed(recent_history):
                    with st.sidebar.expander(f"📌 Session {item['id']} - {item['event_description'][:15]}..."):
                        st.caption(f"Logged: {item['timestamp'][:16]}")
                        st.write(f"**Interests:** {item['interests']}")
                        st.markdown("---")
                        st.write("**Icebreakers:**")
                        for s in item["starters"]:
                            st.write(f"- {s}")
    except Exception:
        st.sidebar.error("Could not communicate with Backend Orchestration Server.")

st.sidebar.markdown("---")
st.sidebar.header("📊 Recent Prompt Feedback Logs")
if st.sidebar.button("Fetch Feedback Analytics", type="secondary"):
    try:
        # Load the mock or real JSON analytics registry stack directly from services
        from backend.app.services import load_feedback_records
        feedback_list = load_feedback_records()
        
        if not feedback_list:
            st.sidebar.info("No explicit downvote/upvote metrics tracked yet.")
        else:
            # Show up to 10 recent feedback entries (double the history limit for granularity)
            recent_feedback = feedback_list[-10:]
            for fb in reversed(recent_feedback):
                # Ternary expression for the icon variable based on action sentiment
                icon = "👍" if fb.get("action") == "like" else "👎"
                
                with st.sidebar.container():
                    st.write(f"{icon} **Prompt:** *\"{fb.get('suggestion_text')[:40]}...\"*")
                    # Subdued caption tracking text hierarchies for metadata processing
                    st.caption(f"Logged timestamp: {fb.get('timestamp')[:19]}")
                    st.markdown("---")
    except Exception:
        st.sidebar.info("Generate icebreakers and upvote/downvote below to populate telemetry tracks.")

# --- CORE APP TABS INTERACTION SECTION ---
tab1, tab2 = st.tabs(["🚀 Conversation Starter Engine", "🔍 Wiki Fact Validator"])

with tab1:
    st.header("Contextual Conversation Prompt Synthesis")
    st.write("Enter your event metrics below to extract zero-shot themes and trigger text generators.")
    
    event_desc = st.text_input("Event Description Summary:", placeholder="e.g., Annual Tech Summit on Clean Energy and Sustainability")
    user_interests = st.text_area("Your Core Competencies & Interests (Comma separated):", placeholder="e.g., AI, blockchain, healthcare")
    
    if st.button("Synthesize Conversation Starters", type="primary"):
        if event_desc.strip() and user_interests.strip():
            with st.spinner("Executing NLP Pipeline Orchestration Steps..."):
                try:
                    cleaned_interests = [i.strip() for i in user_interests.split(',')]
                    joined_interests = ", ".join(cleaned_interests)
                    
                    payload = {"event_description": event_desc, "interests": joined_interests}
                    res = requests.post(f"{BASE_URL}/generate-conversation", json=payload)
                    
                    if res.status_code == 200:
                        data = res.json()
                        st.success("Analysis Complete!")
                        st.subheader("🎯 Discovered Event Themes:")
                        st.write(", ".join(data["extracted_themes"]))
                        
                        st.session_state["active_session_id"] = data["session_id"]
                        st.session_state["last_starters"] = data["starters"]
                except Exception:
                    st.error("Connection drops detected along the backend processing network tier.")
        else:
            st.warning("Please supply valid text contents for both context forms.")

    if "active_session_id" in st.session_state:
        st.markdown("---")
        st.subheader("💡 Suggested Icebreaker Suggestions:")
        for idx, starter in enumerate(st.session_state["last_starters"]):
            st.info(starter)
            col1, col2 = st.columns([1, 10])
            
            if col1.button(f"👍 Upvote {idx+1}", key=f"like_{idx}"):
                try:
                    feedback_payload = {"session_id": st.session_state["active_session_id"], "is_useful": True}
                    requests.post(f"{BASE_URL}/feedback", json=feedback_payload)
                    # Trigger an immediate side-effect fallback entry into service json files
                    from backend.app.services import log_user_feedback
                    log_user_feedback(starter, True)
                    st.toast("Upvote registered inside telemetry logs!")
                except Exception:
                    pass
                    
            if col2.button(f"👎 Downvote {idx+1}", key=f"dislike_{idx}"):
                try:
                    feedback_payload = {"session_id": st.session_state["active_session_id"], "is_useful": False}
                    requests.post(f"{BASE_URL}/feedback", json=feedback_payload)
                    from backend.app.services import log_user_feedback
                    log_user_feedback(starter, False)
                    st.toast("Downvote registered inside telemetry logs!")
                except Exception:
                    pass

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
