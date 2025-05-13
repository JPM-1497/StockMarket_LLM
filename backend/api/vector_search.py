import re
from fastapi import APIRouter, HTTPException, Query
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.stock import Stock
from qdrant_client.models import ScoredPoint
from contextlib import contextmanager

router = APIRouter()
qdrant = QdrantClient(host="qdrant", port=6333)  # Docker service name

try:
    encoder = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    import traceback
    print("🔥 Error loading SentenceTransformer:")
    traceback.print_exc()
    raise

@contextmanager
def get_db():
    """Context-managed DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def highlight(text, query):
    """Bold-matches query terms inside text."""
    terms = query.lower().split()
    for term in terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        text = pattern.sub(lambda m: f"**{m.group(0)}**", text)
    return text

@router.get("/search")
def search_stocks(query: str = Query(..., description="Search query for stock summary")):
    try:
        # Step 1: Embed the query
        query_vector = encoder.encode(query).tolist()

        # Step 2: Query Qdrant
        search_result: list[ScoredPoint] = qdrant.search(
            collection_name="stock_summaries",
            query_vector=query_vector,
            limit=5
        )

        if not search_result:
            return {"matches": []}

        # Step 3: Extract symbols from payload
        matched_symbols = [
            point.payload.get("symbol") for point in search_result
            if point.payload and "symbol" in point.payload
        ]

        with get_db() as db:
            matched_stocks = db.query(Stock).filter(Stock.symbol.in_(matched_symbols)).all()
            stock_lookup = {s.symbol: s for s in matched_stocks}

        # Step 4: Build response
        sorted_results = sorted(search_result, key=lambda x: x.score, reverse=True)
        matches = []
        for point in sorted_results:
            symbol = point.payload.get("symbol")
            if not symbol or symbol not in stock_lookup:
                continue
            stock = stock_lookup[symbol]
            matches.append({
                "symbol": symbol,
                "name": stock.name,
                "summary": highlight(stock.summary, query),
                "score": round(point.score, 4)
            })

        return {
            "query": query,
            "matches": matches
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    return {"status": "ok"}
