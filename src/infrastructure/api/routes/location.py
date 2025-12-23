"""Location API routes."""

from fastapi import APIRouter, HTTPException

from src.application.dto.location_dto import LocationResponse, LocationData
from src.domain.exceptions import LocationNotFoundError

router = APIRouter()


@router.get("/detect", response_model=LocationResponse)
async def detect_location() -> LocationResponse:
    """Detect user location (placeholder for future implementation).
    
    This endpoint is a placeholder. Future implementations could use:
    - IP-based geolocation
    - Browser geolocation API (frontend)
    - GPS coordinates from request headers
    
    Returns:
        LocationResponse with detected location
        
    Raises:
        HTTPException: 501 Not Implemented
    """
    raise HTTPException(
        status_code=501,
        detail="Location detection not yet implemented. Use coordinates or city name.",
    )

