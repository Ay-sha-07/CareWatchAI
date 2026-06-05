"""
Build the ChromaDB vector index from medical guidelines.
Run once before starting the API:
    python -m rag.build_index
"""

import os
import chromadb
from langchain_ibm import WatsonxEmbeddings
from dotenv import load_dotenv

load_dotenv()

GUIDELINES = [
    {
        "id": "who_diabetes_1",
        "text": "WHO guideline: Fasting blood glucose ≥126 mg/dL on two separate occasions confirms diabetes mellitus. Postprandial glucose ≥200 mg/dL with symptoms is also diagnostic.",
        "source": "WHO",
    },
    {
        "id": "who_diabetes_2",
        "text": "WHO: HbA1c ≥6.5% is a diagnostic criterion for diabetes. Target for management is HbA1c < 7.0% in most adults. Hypoglycaemia threshold is glucose < 70 mg/dL.",
        "source": "WHO",
    },
    {
        "id": "icmr_bp_1",
        "text": "ICMR guideline: Systolic BP 130-139 or diastolic 80-89 mmHg is Stage 1 hypertension. Systolic ≥140 or diastolic ≥90 mmHg is Stage 2. Lifestyle modification is first-line for Stage 1.",
        "source": "ICMR",
    },
    {
        "id": "icmr_bp_2",
        "text": "ICMR: Hypertensive crisis is systolic BP > 180 mmHg. Requires immediate medical evaluation. Antihypertensive therapy indicated for Stage 2 hypertension.",
        "source": "ICMR",
    },
    {
        "id": "aha_cardiac_1",
        "text": "AHA: Resting heart rate > 100 bpm (tachycardia) in cardiac patients warrants clinical evaluation. Heart rate 60-100 bpm is normal at rest. Sustained tachycardia may indicate arrhythmia or cardiac decompensation.",
        "source": "AHA",
    },
    {
        "id": "aha_cardiac_2",
        "text": "AHA: Chest discomfort, shortness of breath, or palpitations alongside elevated heart rate in patients with known heart disease should prompt immediate evaluation. 12-lead ECG recommended.",
        "source": "AHA",
    },
    {
        "id": "who_general_1",
        "text": "WHO: Regular physical activity (150 min/week moderate intensity) reduces risk of cardiovascular disease, type 2 diabetes, and hypertension. Smoking cessation strongly recommended for all chronic disease patients.",
        "source": "WHO",
    },
    {
        "id": "mayo_diabetes_1",
        "text": "Mayo Clinic: For type 2 diabetes, blood glucose goals are: fasting 80-130 mg/dL, post-meal (2hr) < 180 mg/dL. Continuous glucose monitoring recommended for patients on insulin.",
        "source": "Mayo Clinic",
    },
]


def build_index():
    embeddings = WatsonxEmbeddings(
        model_id="ibm/slate-125m-english-rtrvr",
        url=os.getenv("WATSONX_URL"),
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        apikey=os.getenv("WATSONX_API_KEY"),
    )

    db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
    client = chromadb.PersistentClient(path=db_path)

    # Delete and recreate for clean rebuild
    try:
        client.delete_collection("medical_guidelines")
    except Exception:
        pass

    collection = client.create_collection("medical_guidelines")

    print(f"Embedding {len(GUIDELINES)} guidelines...")
    for g in GUIDELINES:
        emb = embeddings.embed_query(g["text"])
        collection.add(
            ids=[g["id"]],
            embeddings=[emb],
            documents=[g["text"]],
            metadatas=[{"source": g["source"]}],
        )
        print(f"  ✓ {g['id']}")

    print(f"\nIndex built at {db_path} with {len(GUIDELINES)} documents.")


if __name__ == "__main__":
    build_index()
