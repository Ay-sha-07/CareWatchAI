"""
CareWatch AI — FastAPI Backend
Run with: uvicorn api.main:app --reload
"""

import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agents.crew import run_monitoring_pipeline

app = FastAPI(
    title="CareWatch AI",
    description="Agentic Chronic Disease Monitoring System powered by IBM Granite",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _csv_path(patient_id: int) -> str:
    path = os.path.join(DATA_DIR, f"patient_{patient_id}.csv")
    if not os.path.exists(path):
        raise HTTPException(
            status_code=404,
            detail=f"Patient {patient_id} not found. Run data/generate_patients.py first.",
        )
    return path


@app.get("/health")
async def health():
    return {"status": "ok", "service": "CareWatch AI"}


@app.get("/patients")
async def list_patients():
    """List all available patient IDs."""
    files = [f for f in os.listdir(DATA_DIR) if f.startswith("patient_") and f.endswith(".csv")]
    ids = sorted([int(f.replace("patient_", "").replace(".csv", "")) for f in files])
    return {"patient_ids": ids}


@app.get("/patient/{patient_id}/vitals")
async def get_vitals(patient_id: int, limit: int = 50):
    """Return the latest vitals readings for a patient."""
    path = _csv_path(patient_id)
    df = pd.read_csv(path)
    records = df.tail(limit).to_dict("records")
    return {
        "patient_id": patient_id,
        "count": len(records),
        "vitals": records,
    }


@app.get("/patient/{patient_id}/monitor")
async def monitor_patient(patient_id: int):
    """
    Run the full 4-agent CareWatch pipeline for a patient.
    Returns vitals summary, risk assessment, clinical guidance, and dual-mode alerts.
    """
    path = _csv_path(patient_id)
    result = run_monitoring_pipeline(patient_id, path)
    return result


@app.get("/patient/{patient_id}/summary")
async def get_summary(patient_id: int):
    """Return basic statistics for a patient's vitals."""
    path = _csv_path(patient_id)
    df = pd.read_csv(path)
    return {
        "patient_id": patient_id,
        "condition": df["condition"].iloc[0],
        "total_readings": len(df),
        "anomaly_count": int(df["anomaly"].sum()),
        "stats": {
            "glucose":    {"mean": round(df["glucose"].mean(), 1),    "max": round(df["glucose"].max(), 1),    "min": round(df["glucose"].min(), 1)},
            "bp_sys":     {"mean": round(df["bp_sys"].mean(), 1),     "max": round(df["bp_sys"].max(), 1),     "min": round(df["bp_sys"].min(), 1)},
            "heart_rate": {"mean": round(df["heart_rate"].mean(), 1), "max": round(df["heart_rate"].max(), 1), "min": round(df["heart_rate"].min(), 1)},
        },
    }
