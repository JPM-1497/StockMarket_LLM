# backend/tests/test_semantic_sector_search.py

from services.qdrant_client import qdrant
from services.embedding_encoder import sentence_encoder
from services.semantic_search import semantic_sector_search

def test_sector_queries():
    test_prompts = [
        "top 5 banking companies",
        "strongest energy stocks",
        "leaders in cloud computing",
        "top electric vehicle manufacturers",
        "semiconductor companies in Q1 2025"
    ]

    for prompt in test_prompts:
        print(f"\n🔍 Query: {prompt}")
        results = semantic_sector_search(prompt, qdrant, sentence_encoder, top_k=5)
        for res in results:
            print(f"  ✅ {res['symbol']} - {res['name']} ({res['sector']}) | Score: {res['score']}")

if __name__ == "__main__":
    test_sector_queries()
