from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, strategies
from api.vector_search import router as vector_search_router  # ✅ New import
<<<<<<< HEAD
from api.semantic_search import router as semantic_search_router
from api.compare import router as compare_router
=======
>>>>>>> b8fb39c1e47ecb3da4bad163fb4f4a234c37e7be

app = FastAPI()

# Allow frontend (adjust as needed for production)
app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=["http://localhost:3000", "http://localhost:5173"], 
=======
    allow_origins=["http://localhost:3000"],
>>>>>>> b8fb39c1e47ecb3da4bad163fb4f4a234c37e7be
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(strategies.router, prefix="/api/strategies", tags=["strategies"])
app.include_router(vector_search_router, prefix="/api", tags=["vector-search"])
<<<<<<< HEAD
app.include_router(semantic_search_router, prefix="/api", tags=["semantic-search"])
app.include_router(compare_router, prefix="/api", tags=["compare"])
=======

>>>>>>> b8fb39c1e47ecb3da4bad163fb4f4a234c37e7be
