from typing import List, Tuple
from sqlalchemy.orm import Session
from models.stock import Stock
from datetime import date
import re
import json
from pathlib import Path

# Load alias map
alias_path = Path(__file__).parent / "stock_alias_map.json"
with open(alias_path, "r") as f:
    alias_map = json.load(f)

# Load industry keyword → tickers map
industry_path = Path(__file__).parent / "industry_ticker_map.json"
with open(industry_path, "r") as f:
    industry_map = json.load(f)

# Invert alias map for lookup (alias → list of symbols)
reversed_map = {}
for symbol, aliases in alias_map.items():
    for alias in aliases:
        alias = alias.lower()
        if alias not in reversed_map:
            reversed_map[alias] = set()
        reversed_map[alias].add(symbol)

def get_industry_tickers(query: str) -> List[str]:
    """
    Scan query for known industry keywords and return mapped tickers.
    """
    query_lower = query.lower()
    matched = []

    for keyword, tickers in industry_map.items():
        if keyword in query_lower:
            matched.extend(tickers)

    return matched

def find_relevant_tickers(
    query: str,
    qdrant_client,
    encoder,
    collection_name: str = "stock_summaries",
    top_k: int = 5,
    score_threshold: float = 0.3
) -> List[str]:
    """
    Use semantic search to find the most relevant stock tickers based on the user's query.
    """
    query_vector = encoder.encode(query).tolist()

    results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
        score_threshold=score_threshold
    )

    return [point.payload["symbol"] for point in results if "symbol" in point.payload]


def extract_tickers_and_dates(
    query: str,
    db: Session,
    qdrant_client=None,
    encoder=None
) -> Tuple[List[str], date, date]:
    """
    Extract relevant stock tickers and year range from the query.
    Supports alias → industry → semantic fallback matching.
    """
    query_lower = query.lower()
    query_words = re.findall(r'\b\w+\b', query_lower)
    matched_symbols = set()

    # Step 1: Alias map — prefer first match if multiple tickers found
    for word in query_words:
        possible = reversed_map.get(word)
        if possible:
            # Choose the first ticker alphabetically (or prioritize by custom logic later)
            sorted_symbols = sorted(possible)
            matched_symbols.add(sorted_symbols[0])


    # Step 2: Industry keyword match (if no aliases found)
    if not matched_symbols:
        industry_matches = get_industry_tickers(query)
        if industry_matches:
            matched_symbols.update(industry_matches)

    # Step 3: Fallback — scan through stock names and symbols
    if not matched_symbols:
        stocks = db.query(Stock).all()
        for stock in stocks:
            symbol = stock.symbol.lower()
            name_tokens = re.findall(r'\b\w+\b', stock.name.lower())

            if re.search(rf'\b{re.escape(symbol)}\b', query_lower):
                matched_symbols.add(stock.symbol)
            elif any(token in query_words for token in name_tokens):
                matched_symbols.add(stock.symbol)

    # Step 4: Semantic fallback
    if not matched_symbols and qdrant_client and encoder:
        matched_symbols.update(find_relevant_tickers(query, qdrant_client, encoder))

    # Step 5: Extract year
    year_match = re.search(r"\b(20[0-2][0-9])\b", query)
    if not year_match:
        raise ValueError("Could not extract valid start and end dates from your query. Try phrasing it like 'compare Tesla and Ford in 2023'.")

    year = int(year_match.group(1))
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    return list(matched_symbols), start_date, end_date
