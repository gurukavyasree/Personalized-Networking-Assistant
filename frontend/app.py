import streamlit as st
import requests

st.set_page_config(page_title="AI Networking Assistant", layout="wide")
BACKEND_URL = "http://127.0.0.1:8080/api"

st.title("🤝 AI-Powered Personalized Networking Assistant")

st.sidebar.header("📜 Saved Session History")
if st.sidebar.button("Refresh History"):
    try:
        response = requests.get(f"{BACKEND_URL}/history")
        if response.status_code == 200:
            history_data = response.json().get("history", [])
            for item in reversed(history_data):
                with st.sidebar.expander(f"📌 {item['event_description'][:20]}..."):
                    st.write(f"**Interests:** {item['interests']}")
                    for starter in item["starters"]:
                        st.write(f"- {starter}")
        else:
            st.sidebar.error("Could not fetch history.")
    except Exception:
        st.sidebar.error("Backend offline.")

tab1, tab2 = st.tabs(["🚀 Conversation Starter Generator", "🔍 Quick Fact Verification"])

with tab1:
    st.header("Generate Icebreakers")
    event_desc = st.text_input("What event are you attending?")
    user_interests = st.text_area("What are your core interests?")
    
    if st.button("Generate Conversation Starters", type="primary"):
        if event_desc.strip() and user_interests.strip():
            try:
                payload = {"event_description": event_desc, "interests": user_interests}
                res = requests.post(f"{BACKEND_URL}/generate-starters", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.success("Analysis Complete!")
                    st.subheader("💡 Your Personalized Starters:")
                    for starter in data.get("starters", []):
                        st.info(starter)
                    st.session_state["last_session_id"] = data.get("session_id")
            except Exception:
                st.error("Network communication failure.")

with tab2:
    st.header("Quick Fact Verification Engine")
    query_topic = st.text_input("Enter a topic keyword to verify:")
    if st.button("Run Fact Verification Search"):
        if query_topic.strip():
            try:
                res = requests.post(f"{BACKEND_URL}/fact-check", json={"topic": query_topic})
                if res.status_code == 200:
                    data = res.json()
                    st.write(data.get("verified_summary"))
            except Exception:
                st.error("Could not communicate with server.")
