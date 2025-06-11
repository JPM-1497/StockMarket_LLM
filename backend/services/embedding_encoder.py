# backend/services/embedding_encoder.py

from sentence_transformers import SentenceTransformer

# Load the same model used in embed_summaries.py
sentence_encoder = SentenceTransformer("all-MiniLM-L6-v2")
