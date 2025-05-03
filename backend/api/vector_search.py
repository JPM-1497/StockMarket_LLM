# backend/api/vector_search.py

import re
from fastapi import APIRouter, HTTPException, Query
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.stock import Stock

router = APIRouter()
qdrant = QdrantClient(host="qdrant", port=6333)  # Docker service name
encoder = SentenceTransformer("all-MiniLM-L6-v2")

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
        search_result = qdrant.search(
            collection_name="stock_summaries",
            query_vector=query_vector,
            limit=5
        )

        if not search_result:
            return {"matches": []}

        # Step 3: Get matching stock symbols from payload
        db: Session = SessionLocal()
        matched_symbols = [point.payload["symbol"] for point in search_result]
        matched_stocks = db.query(Stock).filter(Stock.symbol.in_(matched_symbols)).all()
        db.close()

        return {
            "query": query,
            "matches": [
                {
                    "symbol": point.payload["symbol"],
                    "name": next((s.name for s in matched_stocks if s.symbol == point.payload["symbol"]), ""),
                    "summary": highlight(
                        next((s.summary for s in matched_stocks if s.symbol == point.payload["symbol"]), ""),
                        query
                    ),
                    "score": round(point.score, 4)
                }
                for point in search_result
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
