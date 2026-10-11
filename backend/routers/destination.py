from fastapi import APIRouter, HTTPException
from backend.models import DestinationRequest, DestinationResponse
from backend.ai_service import get_destination_info

router = APIRouter()


@router.post("/info", response_model=DestinationResponse)
async def destination_info(request: DestinationRequest):
    """Get comprehensive information about a travel destination."""
    try:
        info = get_destination_info(destination=request.destination)
        return DestinationResponse(destination=request.destination, info=info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch destination info: {str(e)}")
