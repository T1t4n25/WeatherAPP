"""FastAPI dependencies for dependency injection."""

import httpx

from src.application.services.weather_service import WeatherService
from src.infrastructure.config.settings import Settings, get_settings
from src.infrastructure.external.openweather_client import OpenWeatherMapClient


async def get_weather_service() -> WeatherService:
    """Get weather service with dependencies injected.
    
    Returns:
        WeatherService instance
    """
    settings = get_settings()
    client = OpenWeatherMapClient(settings)
    return WeatherService(client)


def get_weather_service_sync() -> WeatherService:
    """Get weather service (sync version for FastAPI dependency).
    
    This creates the service but doesn't await anything.
    The actual HTTP client will be used asynchronously in handlers.
    
    Returns:
        WeatherService instance
    """
    settings = get_settings()
    client = OpenWeatherMapClient(settings)
    return WeatherService(client)

