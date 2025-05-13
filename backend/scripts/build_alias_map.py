# backend/scripts/build_alias_map.py

import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import SearchRequest
import os

# Load your alias queries (e.g., Google, Pharma, Streaming company)
ALIAS_QUERY_FILE = "data/alias_queries.json"
OUTPUT_FILE = "data/stock_alias_map.json"
COLLECTION_NAME = "stock_summaries"

model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(host="qdrant", port=6333)

def load_alias_queries(path: str):
    with open(path, "r") as f:
        return json.load(f)

def build_alias_map(aliases):
    alias_map = {}
    for alias in aliases:
        print(f"🔍 Searching for alias: {alias}")
        query_vector = model.encode(alias).tolist()

        results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=5  # You can increase this if needed
        )

        matched_tickers = []
        for res in results:
            symbol = res.payload.get("symbol")
            if symbol and symbol not in matched_tickers:
                matched_tickers.append(symbol)

        alias_map[alias.lower()] = matched_tickers
        print(f"→ {alias}: {matched_tickers}")

    return alias_map

if __name__ == "__main__":
    if not os.path.exists(ALIAS_QUERY_FILE):
        raise FileNotFoundError(f"Missing alias file: {ALIAS_QUERY_FILE}")

    aliases = load_alias_queries(ALIAS_QUERY_FILE)
    alias_map = build_alias_map(aliases)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(alias_map, f, indent=2)

    print(f"\n✅ Alias map saved to: {OUTPUT_FILE}")
