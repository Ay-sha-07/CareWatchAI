"""
RAG Knowledge Agent — retrieves evidence-based clinical guidelines.
"""

from crewai import Agent, Task
from rag.retriever import retrieve_guidelines


def get_rag_agent() -> Agent:
    return Agent(
        role="Clinical Knowledge Specialist",
        goal="Retrieve and apply evidence-based clinical guidelines relevant to the patient's condition.",
        backstory=(
            "You are trained on WHO, ICMR, AHA, and Mayo Clinic medical guidelines. "
            "You ground every recommendation in verified clinical sources, reducing the "
            "risk of AI hallucination in high-stakes medical contexts."
        ),
        verbose=True,
        allow_delegation=False,
    )


def create_rag_task(agent: Agent, risk_assessment: str) -> Task:
    # Retrieve relevant guidelines at task-creation time
    guidelines = retrieve_guidelines(risk_assessment, k=3)
    guidelines_text = "\n".join(f"  • {g}" for g in guidelines)

    return Task(
        description=f"""
You have retrieved the following clinical guidelines relevant to this patient's situation:

{guidelines_text}

Risk Assessment from the Analysis Agent:
{risk_assessment}

Using ONLY the guidelines above (do not invent information), provide:
1. What the guidelines say about the current readings/risk level
2. Recommended interventions or monitoring steps
3. Any thresholds or red-flag criteria the patient is approaching or has crossed
4. Lifestyle or medication considerations mentioned in guidelines

Always cite the source (WHO / ICMR / AHA / Mayo Clinic) for each point.
""",
        agent=agent,
        expected_output=(
            "Evidence-based clinical guidance with source citations, "
            "grounded strictly in the retrieved guidelines."
        ),
    )
