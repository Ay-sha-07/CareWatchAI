"""
CareWatch AI — CrewAI Orchestrator
Runs the full 4-agent pipeline for a given patient.
"""

import os
from crewai import Crew, Process
from langchain_ibm import WatsonxLLM
from dotenv import load_dotenv

from agents.ingestion_agent import get_ingestion_agent, create_ingestion_task
from agents.analysis_agent  import get_analysis_agent,  create_analysis_task
from agents.rag_agent        import get_rag_agent,        create_rag_task
from agents.alert_agent      import get_alert_agent,      create_alert_task

load_dotenv()


def _build_llm() -> WatsonxLLM:
    return WatsonxLLM(
        model_id="ibm/granite-3-2-8b-instruct",
        url=os.getenv("WATSONX_URL"),
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        apikey=os.getenv("WATSONX_API_KEY"),
        params={
            "max_new_tokens": 1024,
            "temperature": 0.1,
            "repetition_penalty": 1.1,
        },
    )


def run_monitoring_pipeline(patient_id: int, csv_path: str) -> dict:
    """
    Run the full CareWatch multi-agent pipeline for one patient.

    Returns a dict with:
      - patient_id
      - vitals_summary   (Ingestion Agent output)
      - risk_assessment  (Analysis Agent output)
      - clinical_guidance (RAG Agent output)
      - alerts           (Alert Agent output — patient + doctor sections)
    """
    llm = _build_llm()

    # --- Agents ---
    ingestion_agent = get_ingestion_agent()
    analysis_agent  = get_analysis_agent()
    rag_agent       = get_rag_agent()
    alert_agent     = get_alert_agent()

    for agent in [ingestion_agent, analysis_agent, rag_agent, alert_agent]:
        agent.llm = llm

    # --- Tasks (sequential; each receives context from previous) ---
    t1_ingest   = create_ingestion_task(ingestion_agent, csv_path)
    t2_analysis = create_analysis_task(analysis_agent, "{{t1_ingest.output}}")
    t3_rag      = create_rag_task(rag_agent, "{{t2_analysis.output}}")
    t4_alert    = create_alert_task(
        alert_agent,
        "{{t2_analysis.output}}",
        "{{t3_rag.output}}",
        patient_id,
    )

    # Wire context dependencies
    t2_analysis.context = [t1_ingest]
    t3_rag.context      = [t2_analysis]
    t4_alert.context    = [t2_analysis, t3_rag]

    crew = Crew(
        agents=[ingestion_agent, analysis_agent, rag_agent, alert_agent],
        tasks=[t1_ingest, t2_analysis, t3_rag, t4_alert],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return {
        "patient_id":        patient_id,
        "vitals_summary":    str(t1_ingest.output)   if hasattr(t1_ingest,   "output") else "",
        "risk_assessment":   str(t2_analysis.output) if hasattr(t2_analysis, "output") else "",
        "clinical_guidance": str(t3_rag.output)      if hasattr(t3_rag,      "output") else "",
        "alerts":            str(result),
    }
