<<<<<<< HEAD
# backend/scripts/embed_summaries.py

=======
>>>>>>> b8fb39c1e47ecb3da4bad163fb4f4a234c37e7be
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.stock import Stock

<<<<<<< HEAD
# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Qdrant (container name inside Docker)
client = QdrantClient(host="qdrant", port=6333)

# Load stocks with non-null summaries
db: Session = SessionLocal()
stocks = db.query(Stock).filter(Stock.summary.isnot(None)).all()

# Build vectorized points with correct payload
=======
model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host="qdrant", port=6333)  # important: use container name

db: Session = SessionLocal()
stocks = db.query(Stock).filter(Stock.summary.isnot(None)).all()

>>>>>>> b8fb39c1e47ecb3da4bad163fb4f4a234c37e7be
points = []
for idx, stock in enumerate(stocks):
    vector = model.encode(stock.summary).tolist()
    points.append(PointStruct(
<<<<<<< HEAD
        id=idx,  # optional Qdrant internal id
        vector=vector,
        payload={
            "id": stock.id,              # ✅ Enables lookup from DB
            "symbol": stock.symbol,
            "summary": stock.summary
        }
    ))

# Recreate collection
collection_name = "stock_summaries"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=len(points[0].vector),
        distance=Distance.COSINE
    )
)

# Insert vectors
=======
        id=idx,
        vector=vector,
        payload={"symbol": stock.symbol, "summary": stock.summary}
    ))

collection_name = "stock_summaries"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=len(points[0].vector), distance=Distance.COSINE)
)

>>>>>>> b8fb39c1e47ecb3da4bad163fb4f4a234c37e7be
client.upsert(collection_name=collection_name, points=points)
print("✅ Successfully embedded and stored summaries.")
