# 🤝 AI-Powered Personalized Networking Assistant

An interactive, full-stack AI platform built to optimize professional networking communication, zero-shot event theme extraction, and defensive factual validation.

## 🚀 Live Application
The project is deployed and accessible live in the cloud:
👉 **[Launch Live Streamlit Application](https://personalized-networking-assistant-ewzvg4hjsspu9nebfr7map.streamlit.app/)**

---

## 📋 Table of Contents
* [Project Overview](#-project-overview)
* [System Core Features](#-system-core-features)
* [Technical Architecture & Model Selection](#-technical-architecture--model-selection)
* [Project Structure](#-project-structure)
* [Conclusion](#-conclusion)

---

## 🔍 Project Overview
The Personalized Networking Assistant represents a complete and successful implementation of an AI-powered networking support system designed to enhance professional communication and user confidence during networking events. The project was developed through a structured and systematic approach divided into five major Epics, beginning with research and model evaluation, followed by system architecture design, backend API development, frontend interface creation, integration of AI services, and finally testing and deployment. This step-by-step methodology ensured that every component of the application was carefully planned, implemented, and validated before moving to the next stage of development.

---

## ⚙️ System Core Features
* **Contextual Conversation Prompt Synthesis:** Evaluates event description data inputs to automatically configure zero-shot keyword themes targeted directly around user interest profiles.
* **Defensive Fact Verification Module:** Safely queries public knowledge registries (Wikipedia API) using custom request header parameters to provide fast factual references.
* **Telemetry & Session Logs:** Monitors structural interface history tracking logs along with active prompt upvote/downvote action items within the dashboard view.

---

## 🛠️ Technical Architecture & Model Selection
One of the major strengths of the project lies in the selection of technologies and frameworks that balance performance, usability, and deployment feasibility:

* **DistilBERT:** Chosen as the primary zero-shot classification model due to its lightweight architecture, fast inference speed, and reliable contextual understanding capabilities.
* **GPT-2 Small:** Integrated for conversation starter generation because it provides efficient natural language generation while remaining suitable for systems with limited computational resources.
* **FastAPI:** Selected for backend development because of its high performance, asynchronous capabilities, and strong support for API documentation and type validation.
* **Streamlit:** Enabled rapid frontend development and provided an intuitive user interface that supports real-time interaction with minimal complexity.

---

## 📁 Project Structure
```text
Personalized-Networking-Assistant/
├── backend/
│   └── app/
│       ├── main.py          # FastAPI application server
│       └── services.py      # Core NLP algorithms & data processors
├── frontend/
│   └── app.py            # Streamlit Dashboard UI configuration
├── tests/
│   └── test_main.py      # Unit testing validations
├── requirements.txt      # Project library dependency declarations
└── README.md             # Project documentation manual
