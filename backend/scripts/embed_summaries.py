from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.stock import Stock

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host="qdrant", port=6333)  # important: use container name

db: Session = SessionLocal()
stocks = db.query(Stock).filter(Stock.summary.isnot(None)).all()

points = []
for idx, stock in enumerate(stocks):
    vector = model.encode(stock.summary).tolist()
    points.append(PointStruct(
        id=idx,
        vector=vector,
        payload={"symbol": stock.symbol, "summary": stock.summary}
    ))

collection_name = "stock_summaries"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=len(points[0].vector), distance=Distance.COSINE)
)

client.upsert(collection_name=collection_name, points=points)
print("✅ Successfully embedded and stored summaries.")
