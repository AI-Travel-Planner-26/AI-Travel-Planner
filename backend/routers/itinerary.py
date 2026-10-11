from fastapi import APIRouter, HTTPException
from backend.models import (
    RefineRequest,
    RefineResponse,
    PackingListRequest,
    PackingListResponse,
)
from backend.ai_service import refine_itinerary, suggest_packing_list

router = APIRouter()


@router.post("/refine", response_model=RefineResponse)
async def refine_travel_itinerary(request: RefineRequest):
    """Refine an existing itinerary based on user feedback."""
    try:
        refined = refine_itinerary(
            original_itinerary=request.original_itinerary,
            feedback=request.feedback,
        )
        return RefineResponse(refined_itinerary=refined)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refine itinerary: {str(e)}")


@router.post("/packing-list", response_model=PackingListResponse)
async def get_packing_list(request: PackingListRequest):
    """Generate a personalized packing list for a trip."""
    try:
        packing_list = suggest_packing_list(
            destination=request.destination,
            duration=request.duration,
            travel_style=request.travel_style,
            season=request.season,
        )
        return PackingListResponse(
            destination=request.destination,
            packing_list=packing_list,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate packing list: {str(e)}")
