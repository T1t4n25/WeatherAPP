"""Weather API routes."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.application.dto.weather_dto import WeatherResponse
from src.application.services.weather_service import WeatherService
from src.domain.exceptions import InvalidCoordinatesError, WeatherAPIError
from src.infrastructure.api.dependencies import get_weather_service_sync
from src.infrastructure.external.openweather_client import OpenWeatherMapClient
from src.infrastructure.config.settings import get_settings

router = APIRouter()


class CityRequest(BaseModel):
    """City request model."""

    city: str


@router.get("/current", response_model=WeatherResponse)
async def get_current_weather(
    lat: float,
    lon: float,
    service: WeatherService = Depends(get_weather_service_sync),
) -> WeatherResponse:
    """Get current weather by coordinates.
    
    Args:
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
        service: Weather service (injected)
        
    Returns:
        WeatherResponse with current weather data
        
    Raises:
        HTTPException: 422 for invalid coordinates, 503 for API errors
    """
    try:
        weather_data = await service.get_weather_by_coordinates(lat, lon)
        return WeatherResponse(data=weather_data)
    except InvalidCoordinatesError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except WeatherAPIError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e


@router.post("/by-city", response_model=WeatherResponse)
async def get_weather_by_city(
    request: CityRequest,
    service: WeatherService = Depends(get_weather_service_sync),
) -> WeatherResponse:
    """Get weather by city name.
    
    Args:
        request: City request containing city name
        service: Weather service (injected)
        
    Returns:
        WeatherResponse with current weather data
        
    Raises:
        HTTPException: 404 for city not found, 503 for API errors
    """
    try:
        settings = get_settings()
        client = OpenWeatherMapClient(settings)
        lat, lon = await client.get_coordinates_by_city(request.city)

        # Get weather by coordinates
        weather_data = await service.get_weather_by_coordinates(lat, lon)
        return WeatherResponse(data=weather_data)
    except WeatherAPIError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e)) from e
        raise HTTPException(status_code=503, detail=str(e)) from e
    except InvalidCoordinatesError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

