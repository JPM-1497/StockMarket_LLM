# backend/services/semantic_ranker.py

from services.qdrant_client import qdrant
from services.embedding_encoder import sentence_encoder
from services.sql_data_fetcher import get_stock_performance_data
from models.stock import Stock
from db.session import SessionLocal
from datetime import date
from typing import List, Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)

def get_top_performers_from_semantic_match(
    query: str,
    start_date: date,
    end_date: date,
    top_k: int = 5
) -> Tuple[List[str], Dict[str, dict]]:
    """
    Given a semantic query like 'top financial companies', return the best performing stocks.
    """
    db = SessionLocal()
    logging.info(f"🧠 Semantic filtering for query: {query}")

    # Step 1: Embed the query
    vector = sentence_encoder.encode(query).tolist()

    # Step 2: Semantic search for matching stocks
    search_results = qdrant.search(
        collection_name="stock_summaries",
        query_vector=vector,
        limit=50,
        with_payload=True,
        score_threshold=0.3
    )

    candidate_symbols = [point.payload["symbol"] for point in search_results if "symbol" in point.payload]
    logging.info(f"🔍 Found {len(candidate_symbols)} candidate tickers from semantic search")

    # Step 3: Fetch performance data
    performance_data = get_stock_performance_data(db, candidate_symbols, start_date, end_date)

    # Step 4: Filter out stocks without performance data
    performance_data = {
        symbol: data for symbol, data in performance_data.items()
        if data.get("pct_change") is not None
    }

    # Step 5: Rank by % change descending
    sorted_by_performance = sorted(
        performance_data.items(),
        key=lambda x: x[1]["pct_change"],
        reverse=True
    )

    # Step 6: Return top N
    top_results = dict(sorted_by_performance[:top_k])
    top_symbols = list(top_results.keys())
    logging.info(f"🏆 Top {top_k} stocks: {top_symbols}")

    return top_symbols, top_results
