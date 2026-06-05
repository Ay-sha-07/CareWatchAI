"""
Ingestion Agent — normalizes and validates incoming patient vitals.
"""

import pandas as pd
from crewai import Agent, Task

NORMAL_RANGES = {
    "glucose":    (70, 140),
    "bp_sys":     (90, 120),
    "heart_rate": (60, 100),
}


def get_ingestion_agent() -> Agent:
    return Agent(
        role="Health Data Ingestion Specialist",
        goal="Normalize and validate incoming patient vitals, flagging any readings outside normal ranges.",
        backstory=(
            "You are an expert biomedical data engineer specializing in processing "
            "wearable sensor streams. You ensure data quality and produce clean, "
            "structured summaries that downstream agents can reason about."
        ),
        verbose=True,
        allow_delegation=False,
    )


def create_ingestion_task(agent: Agent, patient_csv_path: str) -> Task:
    df = pd.read_csv(patient_csv_path).tail(10)
    records = df[["timestamp", "glucose", "bp_sys", "heart_rate", "condition"]].to_dict("records")

    flags = []
    for r in records:
        for metric, (lo, hi) in NORMAL_RANGES.items():
            val = r.get(metric)
            if val is not None:
                if val > hi:
                    flags.append(f"{metric}={val} (HIGH, normal ≤{hi})")
                elif val < lo:
                    flags.append(f"{metric}={val} (LOW, normal ≥{lo})")

    return Task(
        description=f"""
You are analyzing the latest 10 vitals readings for a patient with condition: {records[0]['condition']}.

Raw readings:
{records}

Normal ranges:
- Glucose: 70–140 mg/dL
- Systolic BP: 90–120 mmHg
- Heart rate: 60–100 bpm

Pre-detected flags: {flags if flags else 'None'}

Produce a structured summary including:
1. Latest values for each metric
2. Trend direction (stable / rising / falling)
3. List of flagged readings with severity (MILD / MODERATE / SEVERE)
4. Overall data quality assessment
""",
        agent=agent,
        expected_output="Structured JSON-style summary of latest vitals with flags and trends.",
    )
