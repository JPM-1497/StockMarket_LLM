# backend/services/qdrant_client.py

from qdrant_client import QdrantClient

# Use Docker host reference if you're running Qdrant via Docker Compose
qdrant = QdrantClient(host="qdrant", port=6333)
