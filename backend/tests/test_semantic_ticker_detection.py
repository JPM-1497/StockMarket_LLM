# backend/tests/test_semantic_ticker_detection.py

from services.qdrant_client import qdrant
from services.embedding_encoder import sentence_encoder
from utils.query_parser import find_relevant_tickers

def test_queries():
    
    print("🚀 Running semantic ticker detection test...")

    test_cases = [
        "Compare Tesla and Ford in 2023",
        "Which AI companies are doing well?",
        "Top electric vehicle stocks this year",
        "How did streaming services perform in 2022?",
        "What are the best semiconductor companies to invest in?",
        "Retail companies with strong growth in 2023",
        "Fintech performance last year"
    ]

    for query in test_cases:
        print(f"\n🔍 Prompt: {query}")
        tickers = find_relevant_tickers(query, qdrant, sentence_encoder, top_k=5)
        print(f"🎯 Matched Tickers: {tickers}")

if __name__ == "__main__":
    test_queries()
