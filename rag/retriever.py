"""
RAG retriever — query ChromaDB for relevant clinical guidelines.
"""

import os
import chromadb
from langchain_ibm import WatsonxEmbeddings
from dotenv import load_dotenv

load_dotenv()

_client = None
_collection = None
_embeddings = None


def _init():
    global _client, _collection, _embeddings
    if _collection is not None:
        return

    _embeddings = WatsonxEmbeddings(
        model_id="ibm/slate-125m-english-rtrvr",
        url=os.getenv("WATSONX_URL"),
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        apikey=os.getenv("WATSONX_API_KEY"),
    )

    db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
    _client = chromadb.PersistentClient(path=db_path)
    _collection = _client.get_collection("medical_guidelines")


def retrieve_guidelines(query: str, k: int = 3) -> list[str]:
    """Return the k most relevant guideline texts for a given query."""
    _init()
    emb = _embeddings.embed_query(query)
    results = _collection.query(query_embeddings=[emb], n_results=k)
    docs = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    return [f"[{src}] {doc}" for src, doc in zip(sources, docs)]
