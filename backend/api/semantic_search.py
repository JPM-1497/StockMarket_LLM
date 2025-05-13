from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import SearchRequest

from models.stock import Stock  # Make sure this path is correct
from db.session import SessionLocal

router = APIRouter()
model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(host="qdrant", port=6333)
COLLECTION_NAME = "stock_summaries"

# ✅ Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/semantic_sector_search")
def semantic_sector_search(
    query: str = Query(...),
    limit: int = 5,
    db: Session = Depends(get_db)
):
    query_vector = model.encode(query).tolist()

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
        with_payload=True  # ✅ Ensures payloads are included in results
    )

    matched = []
    for res in results:
        stock_id = res.payload.get("id")
        if not stock_id:
            continue  # Skip if payload is missing id

        stock = db.query(Stock).filter(Stock.id == stock_id).first()
        if stock:
            matched.append({
                "symbol": stock.symbol,
                "name": stock.name,
                "summary": stock.summary,
                "score": round(res.score, 3)
            })

    return {"matches": matched}
