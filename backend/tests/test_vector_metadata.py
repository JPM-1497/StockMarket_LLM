# backend/tests/test_vector_metadata.py

from services.qdrant_client import qdrant
from services.embedding_encoder import sentence_encoder

def test_summary_vector_metadata():
    test_queries = [
        "top 5 banking companies",
        "leaders in cloud computing",
        "semiconductor companies in Q1 2025",
        "electric vehicle manufacturers",
        "top energy sector stocks"
    ]

    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        query_vector = sentence_encoder.encode(query).tolist()

        results = qdrant.search(
            collection_name="stock_summaries",
            query_vector=query_vector,
            limit=5,
            with_payload=True,
            score_threshold=0.3
        )

        for point in results:
            symbol = point.payload.get("symbol")
            name = point.payload.get("name")
            sector = point.payload.get("sector")
            score = point.score
            print(f"✅ {symbol} - {name} | Sector: {sector} | Score: {score:.4f}")

if __name__ == "__main__":
    test_summary_vector_metadata()
