# 📚 Technical Documentation Manual
## Project: AI-Powered Personalized Networking Assistant

---

## 1. System Overview & Objectives

The **AI-Powered Personalized Networking Assistant** is a full-stack, intelligence-driven software system engineered to optimize professional communication and maximize user confidence during networking events. The application bridges advanced Natural Language Processing (NLP) models with interactive web frameworks to allow users to bypass generic templates, generating context-aware icebreakers targeted directly around a user's skills and active event descriptions. 

Additionally, the architecture establishes a defensive external knowledge-verification layer to demystify complex real-world topics instantly without risk of standard firewall blockages.

### Core Objectives:
* **Context Optimization:** Dynamically analyze multi-topic event descriptions against custom user background parameters to find strong professional intersections.
* **Zero-Shot Theme Extraction:** Eliminate the need for massive labeled training sets by leveraging pre-trained weights (`DistilBERT`) for real-time text classification.
* **Generative Hook Synthesis:** Utilize language generation assets (`GPT-2 Small`) to draft natural, target-specific conversational hooks.
* **Defensive API Interactions:** Establish resilient external API configurations capable of pulling live data frameworks from the Wikipedia REST API without risking `403 Forbidden` errors.

## 2. Architectural Blueprint

The platform relies on a decoupled design pattern separating the client dashboard presentation layer from the background computing servers.

```text
  +-----------------------------------------------------------+
  |                   Streamlit Frontend UI                   |
  |     (Persistent Session States & Custom CSS Grids)        |
  +-----------------------------+-----------------------------+
                                |
                   (Asynchronous HTTP Requests)
                                |
                                v
  +-----------------------------------------------------------+
  |                    FastAPI Backend Router                 |
  |             (API Gateways & Data Validation)              |
  +-------+-------------------------------------------+-------+
          |                                           |
          v                                           v
+--------------------+                      +--------------------+
|  Hugging Face Core |                      | Wikipedia REST API |
| (DistilBERT/GPT-2) |                      | (Defensive Header) |
+--------------------+                      +--------------------+



## 3. Local Development Environment Setup

Follow these sequential steps to safely deploy the application stack locally on your physical workspace:

### Prerequisites
*   **Python 3.11** or higher installed on your system path.
*   **Git** version control framework installed.
*   **Visual Studio Code** (or your preferred IDE).

### Step-by-Step Installation

#### 1. Clone the Repository
Open your computer's terminal or command prompt and run:
```bash
git clone [https://github.com/gurukavyasree/Personalized-Networking-Assistant.git](https://github.com/gurukavyasree/Personalized-Networking-Assistant.git)
cd Personalized-Networking-Assistant





## 4. Codebase Structural Analysis

The application enforces clean separation of concerns across a highly organized directory structure. Below is the functional breakdown of the key architecture components:

### ⚙️ 1. Backend Service Layer (`backend/app/services.py`)
This module houses the core Natural Language Processing algorithms. It initializes the pipelines for:
*   **Theme Parsing:** Setting up the `DistilBERT` classification wrapper to compare event keywords against the user's specific skill arrays.
*   **Prompt Synthesis:** Using `GPT-2 Small` weights to map those parsed themes into structured conversation starters.

### 🖥️ 2. API Router Layer (`backend/app/main.py`)
Built entirely on top of **FastAPI**, this script serves as the engine's control gateway:
*   It exposes the REST endpoints that the frontend dashboard calls.
*   It handles raw data type enforcement and validation, rejecting inputs that do not meet context string criteria.

### 🎨 3. Interface Client Layer (`frontend/app.py`)
This file controls the responsive **Streamlit** visual user dashboard:
*   **Design System:** Injects the web font (`Inter`) and custom CSS cards to show the AI output elegantly.
*   **State Control:** Manages `st.session_state` arrays to store your active run telemetry logs, ensuring users do not lose their generated text history when refreshing data pages.
