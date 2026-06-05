"""
Alert & Recommendation Agent — generates dual-mode patient and doctor outputs.
"""

from crewai import Agent, Task


def get_alert_agent() -> Agent:
    return Agent(
        role="Medical Communication Specialist",
        goal=(
            "Generate clear, actionable dual-mode alerts: plain-language messages "
            "for patients and structured clinical summaries for doctors."
        ),
        backstory=(
            "You specialize in health communication. You know that patients need "
            "simple, reassuring language with clear action steps, while doctors need "
            "precise clinical language with metrics, trends, and guideline references. "
            "You never cause unnecessary alarm, but you never downplay serious findings."
        ),
        verbose=True,
        allow_delegation=False,
    )


def create_alert_task(
    agent: Agent,
    risk_assessment: str,
    clinical_guidance: str,
    patient_id: int,
) -> Task:
    return Task(
        description=f"""
Patient ID: {patient_id}

Risk Assessment:
{risk_assessment}

Clinical Guidance (evidence-based):
{clinical_guidance}

Generate exactly TWO clearly labeled outputs:

---PATIENT_ALERT---
Write in plain, friendly language (max 4 sentences). No medical jargon.
Explain: what is happening with their health right now, what they should do 
immediately, and whether they need to contact their doctor.
Tone: calm, supportive, clear.

---DOCTOR_SUMMARY---
Write in clinical format. Include:
- Patient ID and risk level
- Key abnormal metrics with exact values
- Trend direction
- Relevant guideline thresholds crossed
- Recommended next clinical steps
- Urgency level (Routine / Within 24h / Immediate)
""",
        agent=agent,
        expected_output=(
            "Two clearly labeled sections: PATIENT_ALERT (plain language) "
            "and DOCTOR_SUMMARY (clinical format)."
        ),
    )
