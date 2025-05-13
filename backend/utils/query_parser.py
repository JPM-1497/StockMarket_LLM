# backend/utils/query_parser.py

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

# Invert alias map for lookup (alias → list of symbols)
reversed_map = {}
for symbol, aliases in alias_map.items():
    for alias in aliases:
        alias = alias.lower()
        if alias not in reversed_map:
            reversed_map[alias] = set()
        reversed_map[alias].add(symbol)

def extract_tickers_and_dates(query: str, db: Session) -> Tuple[List[str], date, date]:
    query_lower = query.lower()
    query_words = re.findall(r'\b\w+\b', query_lower)
    matched_symbols = set()

    # Step 1: Match via alias map — only use aliases that map to 1 symbol
    for word in query_words:
        possible = reversed_map.get(word)
        if possible and len(possible) == 1:
            matched_symbols.update(possible)

    # Step 2: Fallback — scan through stock names and symbols
    if not matched_symbols:
        stocks = db.query(Stock).all()
        for stock in stocks:
            symbol = stock.symbol.lower()
            name_tokens = re.findall(r'\b\w+\b', stock.name.lower())

            if re.search(rf'\b{re.escape(symbol)}\b', query_lower):
                matched_symbols.add(stock.symbol)
            elif any(token in query_words for token in name_tokens):
                matched_symbols.add(stock.symbol)

    # Extract year from query
    year_match = re.search(r"\b(20[0-2][0-9])\b", query)
    if not year_match:
        raise ValueError("Could not extract valid start and end dates from your query. Try phrasing it like 'compare Tesla and Ford in 2023'.")

    year = int(year_match.group(1))
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    return list(matched_symbols), start_date, end_date
