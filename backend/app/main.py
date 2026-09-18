from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.environment import router as environment_router

app = FastAPI(
    title="EcoMind",
    description="AI Biodiversity Intelligence System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(environment_router)


@app.get("/")
def home():
    return {
        "project": "EcoMind",
        "message": "AI Biodiversity Intelligence System",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}