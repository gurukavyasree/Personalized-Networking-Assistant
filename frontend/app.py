import sys
from pathlib import Path

# --- DYNAMIC PYTHON PATH MANIPULATION ---
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import uuid
from datetime import datetime

# --- DIRECT SERVICE LAYER IMPORTS (Bypasses Localhost Server API) ---
try:
    from backend.app.services import (
        extract_event_themes, 
        generate_topics, 
        fetch_wikipedia_summary,
        log_user_feedback,
        load_feedback_records
    )
    # Mocking history logging locally for cloud environment stability
    if "cloud_history" not in st.session_state:
        st.session_state["cloud_history"] = []
except ImportError:
    st.error("Missing backend service path modules. Verify repository file structure configurations.")

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
    history_records = st.session_state.get("cloud_history", [])
    if not history_records:
        st.sidebar.info("No transaction logs archived yet.")
    else:
        recent_history = history_records[-5:]
        for item in reversed(recent_history):
            with st.sidebar.expander(f"📌 Session {item['id'][:8]}..."):
                st.caption(f"Logged: {item['timestamp']}")
                st.write(f"**Interests:** {item['interests']}")
                st.markdown("---")
                st.write("**Icebreakers:**")
                for s in item["starters"]:
                    st.write(f"- {s}")

st.sidebar.markdown("---")
st.sidebar.header("📊 Recent Prompt Feedback Logs")
if st.sidebar.button("Fetch Feedback Analytics", type="secondary"):
    try:
        feedback_list = load_feedback_records()
        if not feedback_list:
            st.sidebar.info("No explicit downvote/upvote metrics tracked yet.")
        else:
            recent_feedback = feedback_list[-10:]
            for fb in reversed(recent_feedback):
                icon = "👍" if fb.get("action") == "like" else "👎"
                with st.sidebar.container():
                    st.write(f"{icon} **Prompt:** *\"{fb.get('suggestion_text')[:40]}...\"*")
                    st.caption(f"Logged: {fb.get('timestamp')[:19]}")
                    st.markdown("---")
    except Exception:
        st.sidebar.info("Generate icebreakers and rate them below to populate telemetry tracks.")

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
                    # Execute services directly in-process
                    candidate_labels = ["AI", "healthcare", "blockchain", "education", "sustainability"]
                    extracted = extract_event_themes(event_desc, candidate_labels)
                    starters = generate_topics(extracted, user_interests)
                    session_id = str(uuid.uuid4())
                    
                    st.session_state["active_session_id"] = session_id
                    st.session_state["last_starters"] = starters
                    
                    # Log into session state history
                    st.session_state["cloud_history"].append({
                        "id": session_id,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "event_description": event_desc,
                        "interests": user_interests,
                        "starters": starters
                    })
                    st.success("Analysis Complete!")
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")
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
                    log_user_feedback(starter, True)
                    st.toast("Upvote registered inside telemetry logs!")
                except Exception:
                    pass
                    
            if col2.button(f"👎 Downvote {idx+1}", key=f"dislike_{idx}"):
                try:
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
                    summary = fetch_wikipedia_summary(topic_query)
                    st.success("Verification Complete!")
                    st.info(summary)
                except Exception as e:
                    st.error(f"Verification processing engine error: {str(e)}")
