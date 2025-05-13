# backend/services/semantic_search.py

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest, Filter, FieldCondition, MatchValue

# Initialize once (use caching/DI in production)
model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(host="qdrant", port=6333)

COLLECTION_NAME = "stock_summaries"

def semantic_sector_search(user_query: str, top_k: int = 5):
    """
    Embed the user query and perform semantic search in Qdrant to find related stocks.

    Returns:
        List of dicts: [{"symbol": "AAPL", "summary": "...", "score": 0.89}, ...]
    """
    embedded_query = model.encode(user_query).tolist()

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedded_query,
        limit=top_k,
        with_payload=True
    )

    return [
        {
            "symbol": hit.payload.get("symbol"),
            "name": hit.payload.get("name"),
            "summary": hit.payload.get("summary"),
            "score": hit.score
        }
        for hit in results
    ]
