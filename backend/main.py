from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import planner, destination, itinerary

app = FastAPI(
    title="AI Travel Planner API",
    description="Backend API for the AI-powered travel planning application",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(planner.router, prefix="/api/planner", tags=["Planner"])
app.include_router(destination.router, prefix="/api/destination", tags=["Destination"])
app.include_router(itinerary.router, prefix="/api/itinerary", tags=["Itinerary"])


@app.get("/")
def root():
    return {"message": "AI Travel Planner API is running 🌍"}


@app.get("/health")
def health():
    return {"status": "ok"}
