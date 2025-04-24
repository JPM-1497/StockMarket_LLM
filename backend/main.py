from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth  # your first router

app = FastAPI()

# Allow frontend (adjust as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
