"""
Analysis Agent — anomaly detection and risk assessment.
"""

from crewai import Agent, Task


def get_analysis_agent() -> Agent:
    return Agent(
        role="Medical Data Analyst",
        goal="Detect anomalies and trends in patient vitals and produce a risk assessment.",
        backstory=(
            "You are a specialist in time-series biomedical analytics. You interpret "
            "patterns in patient health data, identify early warning signs of deterioration, "
            "and produce clear risk assessments that guide clinical decisions."
        ),
        verbose=True,
        allow_delegation=False,
    )


def create_analysis_task(agent: Agent, vitals_summary: str) -> Task:
    return Task(
        description=f"""
You are analyzing a vitals summary to assess patient risk.

Vitals Summary:
{vitals_summary}

Perform the following analysis:
1. Identify any critically abnormal values (life-threatening thresholds)
2. Assess whether values are improving, stable, or deteriorating
3. Assign an overall RISK LEVEL: LOW / MEDIUM / HIGH / CRITICAL
4. Identify which underlying condition appears to be worsening
5. Estimate urgency: routine monitoring / contact doctor within 24h / seek immediate care

Be precise and concise. Use medical terminology appropriately.
""",
        agent=agent,
        expected_output=(
            "Risk assessment with: risk level (LOW/MEDIUM/HIGH/CRITICAL), "
            "key findings, condition status, and urgency recommendation."
        ),
    )
