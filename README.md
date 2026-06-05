# 🫀 CareWatch AI — Chronic Disease Monitoring Agent

**IBM SkillsBuild University Engagement · AICTE 2026 · Problem Statement #27**

An agentic AI system that monitors patients with chronic diseases (diabetes, hypertension, cardiac conditions) in real time using multi-agent orchestration, RAG-grounded medical knowledge, and IBM Granite on watsonx.ai.

---

## Architecture

```
Wearable Data / EHR
        │
        ▼
┌─────────────────┐     ┌─────────────────┐
│  Ingestion Agent│────▶│  Analysis Agent │
│  (normalizes)   │     │  (anomaly detect│
└─────────────────┘     └────────┬────────┘
                                  │
                    ┌─────────────▼────────────┐
                    │   RAG Knowledge Agent     │
                    │  (WHO / ICMR / AHA /      │
                    │   Mayo Clinic guidelines) │
                    └─────────────┬────────────┘
                                  │
                    ┌─────────────▼────────────┐
                    │  Alert & Report Agent     │
                    │  Patient alert + Doctor   │
                    │  clinical summary         │
                    └──────────────────────────┘
```

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
git clone https://github.com/YOUR_USERNAME/carewatch-ai
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

## IBM Submission Checklist

- [x] `app.json` — project metadata
- [ ] `yourproblemstatement.pdf` — export your PPTX as PDF and rename
- [ ] `CareWatch_AI_Chronic_Disease_Monitoring.pptx` — filled submission template
- [ ] All source code files (this repo)

---

*Built for IBM SkillsBuild University Engagement · AICTE 2026*
