# 🫀 CareWatch AI — Chronic Disease Monitoring Agent

**IBM SkillsBuild University Engagement · AICTE 2026 · Problem Statement #27**

The Challenge - An AI agent for chronic disease monitoring helps patients and healthcare providers 
manage long-term conditions effectively. 
It continuously analyzes health data from wearables, medical records, and patient inputs to detect early 
warning signs. 
Using AI and predictive analytics, it offers personalized insights, medication reminders, and lifestyle 
recommendations. 
The agent supports diseases like diabetes, hypertension, and heart conditions with real-time monitoring 
and alerts. 
It enables proactive care, reduces hospital visits, and improves patient adherence to treatment plans. 
This intelligent assistant bridges the gap between patients and providers, enhancing chronic care 
outcomes. 
Technology - Use of IBM cloud lite services /IBM Granity is mandatory.

---

## Architecture

Disclaimor: Current prototype stores patient history in CSV files.Future deployment replaces this with Cloudant/PostgreSQL.

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/af112196-9655-488d-8a53-86c5e36e4908" />

## Tech Stack

| Component         | Technology                              |
|-------------------|-----------------------------------------|
| LLM               | IBM Granite (`ibm/granite-3-2-8b-instruct`) |
| AI Platform       | IBM watsonx.ai (Cloud Lite)             |
| Agent Framework   | CrewAI + LangChain                      |
| Vector Database   | ChromaDB                                |
| Embeddings        | IBM Slate (`ibm/slate-125m-english-rtrvr`) |
| Backend           | FastAPI                                 |
| Frontend          | React + Recharts                        |

---

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/ay-sha-07/carewatch-ai
cd carewatch-ai
```

### 2. Set up Python environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure IBM credentials
```bash
cp .env.example .env
# Edit .env and fill in your WATSONX_API_KEY and WATSONX_PROJECT_ID
# Get free credentials at: https://ibm.com/watsonx
```

### 4. Generate synthetic patient data
```bash
python data/generate_patients.py
```

### 5. Build the RAG index
```bash
python -m rag.build_index
```

### 6. Start the backend
```bash
uvicorn api.main:app --reload
# API running at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 7. Start the frontend
```bash
cd frontend
npm install
npm run dev
# Dashboard at http://localhost:5173
```

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /patients` | List all patient IDs |
| `GET /patient/{id}/vitals` | Latest vitals readings |
| `GET /patient/{id}/summary` | Stats and anomaly count |
| `GET /patient/{id}/monitor` | **Run full 4-agent pipeline** |

---

## Project Structure

```
carewatch/
├── agents/
│   ├── ingestion_agent.py   # Normalizes wearable data
│   ├── analysis_agent.py    # Anomaly detection + risk assessment
│   ├── rag_agent.py         # Retrieves clinical guidelines
│   ├── alert_agent.py       # Generates patient + doctor outputs
│   └── crew.py              # CrewAI orchestration
├── rag/
│   ├── build_index.py       # Embeds guidelines into ChromaDB
│   └── retriever.py         # Semantic search on guidelines
├── data/
│   └── generate_patients.py # Synthetic wearable data generator
├── api/
│   └── main.py              # FastAPI backend
├── frontend/
│   └── src/App.jsx          # React dashboard
├── app.json                 # IBM submission metadata
├── requirements.txt
└── .env.example
```
---

*Built for IBM SkillsBuild University Engagement · AICTE 2026*
