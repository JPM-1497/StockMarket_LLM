from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, strategies
from api.vector_search import router as vector_search_router  # ✅ New import
from api.semantic_search import router as semantic_search_router
from api.compare import router as compare_router
from api.news import router as news_router  


app = FastAPI()

# Allow frontend (adjust as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(strategies.router, prefix="/api/strategies", tags=["strategies"])
app.include_router(vector_search_router, prefix="/api", tags=["vector-search"])
app.include_router(semantic_search_router, prefix="/api", tags=["semantic-search"])
app.include_router(compare_router, prefix="/api", tags=["compare"])
app.include_router(news_router, prefix="/api", tags=["news"])