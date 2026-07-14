# 🤝 AI-Powered Personalized Networking Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/NLP--Models-DistilBERT%20%26%20GPT--2-8A2BE2?style=for-the-badge" alt="NLP Models"/>
</p>

An interactive, full-stack AI platform engineered to optimize professional networking communication, run zero-shot event theme extraction, and execute defensive factual validation layer tasks.

---

### 🌐 Cloud Architecture Deployment
The production interface is fully configured and live:
👉 **[Launch Live Platform Workspace](https://personalized-networking-assistant-ewzvg4hjsspu9nebfr7map.streamlit.app/)**

---

## 🗺️ Workspace Navigation
* [Project Overview](#-project-overview)
* [System Architecture & Core Infrastructure](#-system-architecture--core-infrastructure)
* [Core Core Modules](#-core-core-modules)
* [Repository Workspace Map](#-repository-workspace-map)
* [Academic Project Conclusion](#-academic-project-conclusion)

---

## 🔍 Project Overview

> [!NOTE]  
> The Personalized Networking Assistant represents a complete and successful implementation of an AI-powered networking support system designed to enhance professional communication and user confidence during networking events. 

The project was developed through a structured and systematic approach divided into five major Epics, beginning with research and model evaluation, followed by system architecture design, backend API development, frontend interface creation, integration of AI services, and finally testing and deployment. This step-by-step methodology ensured that every component of the application was carefully planned, implemented, and validated before moving to the next stage of development.

---

## 🛠️ System Architecture & Core Infrastructure

One of the major strengths of the project lies in the selection of technologies and frameworks that balance performance, usability, and deployment feasibility:

| Technology Stack | Operational Layer | Strategic Selection Justification |
| :--- | :--- | :--- |
| **DistilBERT** | Machine Learning Core | Chosen as the primary zero-shot classification model due to its lightweight architecture, fast inference speed, and reliable contextual understanding capabilities. |
| **GPT-2 Small** | Text Generation Core | Integrated for conversation starter generation because it provides efficient natural language generation while remaining suitable for systems with limited computational resources. |
| **FastAPI** | Backend API Engine | Selected for backend development because of its high performance, asynchronous capabilities, and strong support for API documentation and type validation. |
| **Streamlit** | Interface Platform | Enabled rapid frontend development and provided an intuitive user interface that supports real-time interaction with minimal complexity. |

---

## ⚙️ Core Core Modules

* **🚀 Contextual Conversation Prompt Synthesis**
  Evaluates raw event description data strings to parse zero-shot keyword themes targeted precisely around custom competency lists.
* **🔍 Defensive Fact Verification Module**
  Safely queries public knowledge networks (Wikipedia REST API layer) passing custom request tracking headers to confidently bypass 403 access rejections.
* **📊 Workspace Telemetry & Session Records**
  Logs workflow interaction records right inside the navigation framework along with active user upvote/downvote analytics features.

---

## 📁 Repository Workspace Map

```text
Personalized-Networking-Assistant/
├── backend/
│   └── app/
│       ├── main.py          # FastAPI application server management
│       └── services.py      # Core NLP algorithms & model configurations
├── frontend/
│   └── app.py            # Premium Streamlit UI & Typography Engine
├── tests/
│   └── test_main.py      # Unit testing validations framework
├── requirements.txt      # Production environment package list
└── README.md             # Polished documentation overview manual
