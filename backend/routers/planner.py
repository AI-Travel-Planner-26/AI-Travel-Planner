from fastapi import APIRouter, HTTPException
from backend.models import TravelPlanRequest, TravelPlanResponse
from backend.ai_service import generate_travel_plan

router = APIRouter()


@router.post("/generate", response_model=TravelPlanResponse)
async def create_travel_plan(request: TravelPlanRequest):
    """Generate a complete AI-powered travel plan."""
    try:
        plan = generate_travel_plan(
            destination=request.destination,
            duration=request.duration,
            budget=request.budget,
            travel_style=request.travel_style,
            interests=request.interests,
            travelers=request.travelers,
        )
        return TravelPlanResponse(
            destination=request.destination,
            duration=request.duration,
            plan=plan,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate travel plan: {str(e)}")
