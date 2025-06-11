# backend/services/semantic_search.py

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from typing import List, Dict

def semantic_sector_search(
    query: str,
    qdrant_client: QdrantClient,
    encoder: SentenceTransformer,
    top_k: int = 10,
    score_threshold: float = 0.35,
    collection_name: str = "stock_summaries"
) -> List[Dict]:
    """
    Performs a semantic search on stock summaries and returns top-matching stock metadata.
    Each result includes symbol, name, sector, and similarity score.
    """
    query_vector = encoder.encode(query).tolist()
    results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
        score_threshold=score_threshold
    )

    matched = []
    for point in results:
        payload = point.payload
        matched.append({
            "symbol": payload.get("symbol"),
            "name": payload.get("name"),
            "sector": payload.get("sector"),
            "score": round(point.score, 4)
        })

    return matched
