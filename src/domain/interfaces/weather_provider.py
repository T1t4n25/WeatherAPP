"""Weather provider interface."""

from typing import Protocol

from src.domain.entities.weather import WeatherData


class WeatherProvider(Protocol):
    """Protocol for weather data providers."""

    async def get_weather(self, lat: float, lon: float) -> WeatherData:
        """Fetch weather data for given coordinates.
        
        Args:
            lat: Latitude in decimal degrees
            lon: Longitude in decimal degrees
            
        Returns:
            WeatherData object with current weather information
            
        Raises:
            WeatherAPIError: If API request fails
            InvalidCoordinatesError: If coordinates are invalid
        """
        ...

