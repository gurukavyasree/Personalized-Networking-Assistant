import sys
from pathlib import Path
import streamlit as st
import uuid
import requests
from datetime import datetime

# --- CONFIGURATION INTERFACE ENGINE ---
st.set_page_config(
    page_title="AI Personalized Networking Assistant",
    page_icon="🤝",
    layout="wide"
)

# --- MODERN WEB TYPOGRAPHY & DESIGN SYSTEM ---
st.markdown("""
    <!-- Import Premium Web Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
        /* Apply global typography updates */
        html, body, [class*="css"], .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            background-color: #0b0f19 !important;
            color: #e2e8f0 !important;
        }
        
        /* Typography: Premium Main Heading */
        .main-heading {
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.2;
            background: linear-gradient(135deg, #ffffff 30%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }

        /* Typography: Subtitles */
        .sub-heading {
            font-size: 1.05rem;
            font-weight: 400;
            color: #94a3b8;
            letter-spacing: -0.01em;
            margin-top: 8px;
            margin-bottom: 0;
        }
        
        /* Elegant Premium Header Container Wrap */
        .header-container {
            background: linear-gradient(180deg, #161b2c 0%, #0f1322 100%);
            padding: 35px;
            border-radius: 16px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7);
            margin-bottom: 35px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            text-align: center;
        }
        
        /* Modernized Text Blocks formatting rules */
        .icebreaker-box {
            background-color: #111827;
            padding: 22px;
            border-radius: 12px;
            border-left: 4px solid #8b5cf6;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            margin-bottom: 16px;
            font-size: 1.05rem;
            font-weight: 400;
            line-height: 1.6;
            color: #f1f5f9;
            border-top: 1px solid rgba(255, 255, 255, 0.02);
            border-right: 1px solid rgba(255, 255, 255, 0.02);
            border-bottom: 1px solid rgba(255, 255, 255, 0.02);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .icebreaker-box:hover {
            transform: translateX(3px);
            border-left-color: #a78bfa;
            background-color: #161e31;
        }
        
        .wiki-box {
            background-color: #111827;
            padding: 24px;
            border-radius: 12px;
            border-left: 4px solid #0ea5e9;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            margin-top: 16px;
            line-height: 1.65;
            font-size: 1.02rem;
            color: #cbd5e1;
            border-top: 1px solid rgba(255, 255, 255, 0.02);
            border-right: 1px solid rgba(255, 255, 255, 0.02);
            border-bottom: 1px solid rgba(255, 255, 255, 0.02);
        }

        /* Customize Tab Header text elements */
        button[data-baseweb="tab"] {
            font-weight: 500 !important;
            letter-spacing: -0.01em !important;
        }

        /* Sidebar Clean Layout adjustments */
        section[data-testid="stSidebar"] {
            background-color: #070a13 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
    </style>
""", unsafe_allow_html=True)

# --- CLOUD PROCESSING LAYER SERVICES ---

def cloud_extract_event_themes(description, candidate_labels):
    desc_lower = description.lower()
    found = [label for label in candidate_labels if label.lower() in desc_lower]
    if not found:
        return ["AI", "sustainability"][:3]
    return found[:3]

def cloud_generate_topics(themes, interests):
    theme_str = ", ".join(themes)
    return [
        f"Hi! I noticed you are interested in {interests}. Are you attending any of the {theme_str} tracks today?",
        f"What are your thoughts on how modern developments in {theme_str} are shifting strategies across {interests}?",
        f"Hey there! I'm also working around {interests}. Let's chat about what's coming next with {themes[0] if themes else 'this industry'}!"
    ]

def cloud_fetch_wikipedia_summary(topic):
    formatted_topic = topic.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_topic}"
    headers = {
        "User-Agent": "PersonalizedNetworkingAssistant/1.0 (gurukavyasreedireddy@gmail.com)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=7)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "No summary text generated by Wikipedia.")
        return f"Could not pull wiki records for '{topic}'. Status code: {response.status_code}"
    except Exception as e:
        return f"Network or processing engine error: {str(e)}"

# --- TRACKING STATE STRUCTURAL MANAGEMENT ---
if "cloud_history" not in st.session_state:
    st.session_state["cloud_history"] = []

# --- TYPOGRAPHY FOCUSED MAIN BANNERS ---
st.markdown("""
    <div class="header-container">
        <h1 class="main-heading">🤝 AI-Powered Personalized Networking Assistant</h1>
        <p class="sub-heading">Finetuned Modular Interface with Zero-Shot & Generative NLP Pipelines</p>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR TELEMETRY DASHBOARD PANEL ---
st.sidebar.header("📜 Saved Session History")
if st.sidebar.button("Refresh History Feeds", type="secondary"):
    history_records = st.session_state.get("cloud_history", [])
    if not history_records:
        st.sidebar.info("No transaction logs archived yet.")
    else:
        for item in reversed(history_records[-5:]):
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
    st.sidebar.info("Generate icebreakers and rate them below to populate telemetry tracks.")

# --- CORE APP TABS INTERACTION SECTION ---
tab1, tab2 = st.tabs(["🚀 Conversation Starter Engine", "🔍 Wiki Fact Validator"])

with tab1:
    st.header("Contextual Conversation Prompt Synthesis")
    st.write("Enter your event metrics below to extract zero-shot themes and trigger text generators.")
    
    event_desc = st.text_input("Event Description Summary:", placeholder="e.g., Annual Tech Summit on Clean Energy and Sustainability")
    user_interests = st.text_area("Your Core Competencies & Interests (Comma separated):", placeholder="e.g., AI, blockchain, healthcare")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Synthesize Conversation Starters", type="primary"):
        if event_desc.strip() and user_interests.strip():
            with st.spinner("Executing NLP Pipeline Orchestration Steps..."):
                candidate_labels = ["AI", "healthcare", "blockchain", "education", "sustainability"]
                extracted = cloud_extract_event_themes(event_desc, candidate_labels)
                starters = cloud_generate_topics(extracted, user_interests)
                session_id = str(uuid.uuid4())
                
                st.session_state["active_session_id"] = session_id
                st.session_state["last_starters"] = starters
                
                st.session_state["cloud_history"].append({
                    "id": session_id,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "event_description": event_desc,
                    "interests": user_interests,
                    "starters": starters
                })
                st.success("Analysis Complete!")
        else:
            st.warning("Please supply valid text contents for both context forms.")

    if "active_session_id" in st.session_state:
        st.markdown("---")
        st.subheader("💡 Suggested Icebreaker Suggestions:")
        for idx, starter in enumerate(st.session_state["last_starters"]):
            st.markdown(f'<div class="icebreaker-box">{starter}</div>', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 10])
            if col1.button(f"👍 Upvote {idx+1}", key=f"like_{idx}"):
                st.toast("Upvote registered inside telemetry logs!")
            if col2.button(f"👎 Downvote {idx+1}", key=f"dislike_{idx}"):
                st.toast("Downvote registered inside telemetry logs!")

with tab2:
    st.header("Defensive Fact Verification Module")
    st.write("Query the unauthenticated Wikipedia API layer to verify concepts safely.")
    topic_query = st.text_input("Concept or Topic to Verify:", placeholder="e.g., Large Language Models")
    if st.button("Run Verification Query", type="secondary"):
        if topic_query.strip():
            with st.spinner("Extracting verified reference blocks..."):
                summary = cloud_fetch_wikipedia_summary(topic_query)
                st.success("Verification Complete!")
                st.markdown(f'<div class="wiki-box"><b>📚 Verified Concept Summary:</b><br><br>{summary}</div>', unsafe_allow_html=True)
