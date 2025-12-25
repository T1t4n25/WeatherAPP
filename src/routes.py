"""API routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.models import WeatherResponse
from src.service import WeatherService

router = APIRouter(prefix="/api/v1/weather", tags=["weather"])

# Create service instance
_weather_service = WeatherService()


class CityRequest(BaseModel):
    """City request model."""
    city: str


@router.get("/current", response_model=WeatherResponse)
async def get_current_weather(lat: float, lon: float) -> WeatherResponse:
    """Get current weather by coordinates."""
    try:
        weather_data = await _weather_service.get_weather_by_coordinates(lat, lon)
        return WeatherResponse(data=weather_data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e


@router.post("/by-city", response_model=WeatherResponse)
async def get_weather_by_city(request: CityRequest) -> WeatherResponse:
    """Get weather by city name."""
    try:
        weather_data = await _weather_service.get_weather_by_city(request.city)
        return WeatherResponse(data=weather_data)
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg) from e
        raise HTTPException(status_code=422, detail=error_msg) from e
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e

