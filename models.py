from pydantic import BaseModel, Field
from typing import Optional


class TravelPlanRequest(BaseModel):
    destination: str = Field(..., description="Travel destination (city or country)")
    duration: int = Field(..., ge=1, le=60, description="Trip duration in days")
    budget: str = Field(..., description="Budget level: Budget / Mid-range / Luxury")
    travel_style: str = Field(..., description="Travel style: Adventure / Relaxation / Cultural / Business / Family")
    interests: list[str] = Field(default=[], description="List of traveler interests")
    travelers: int = Field(default=1, ge=1, le=20, description="Number of travelers")


class TravelPlanResponse(BaseModel):
    destination: str
    duration: int
    plan: str
    status: str = "success"


class DestinationRequest(BaseModel):
    destination: str = Field(..., description="Destination to get info about")


class DestinationResponse(BaseModel):
    destination: str
    info: str
    status: str = "success"


class RefineRequest(BaseModel):
    original_itinerary: str = Field(..., description="The original itinerary text")
    feedback: str = Field(..., description="User feedback or change requests")


class RefineResponse(BaseModel):
    refined_itinerary: str
    status: str = "success"


class PackingListRequest(BaseModel):
    destination: str
    duration: int = Field(..., ge=1, le=60)
    travel_style: str
    season: str = Field(..., description="Season: Spring / Summer / Autumn / Winter")


class PackingListResponse(BaseModel):
    destination: str
    packing_list: str
    status: str = "success"
