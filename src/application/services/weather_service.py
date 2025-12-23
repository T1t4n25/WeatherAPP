"""Weather service for business logic."""

from src.domain.entities.weather import WeatherData
from src.domain.exceptions import InvalidCoordinatesError, WeatherAPIError
from src.domain.interfaces.weather_provider import WeatherProvider


class WeatherService:
    """Service for weather-related business logic."""

    def __init__(self, weather_provider: WeatherProvider) -> None:
        """Initialize weather service.
        
        Args:
            weather_provider: Weather provider implementation
        """
        self._provider = weather_provider

    async def get_weather_by_coordinates(
        self, lat: float, lon: float
    ) -> WeatherData:
        """Get weather data by coordinates.
        
        Args:
            lat: Latitude in decimal degrees
            lon: Longitude in decimal degrees
            
        Returns:
            WeatherData object with current weather
            
        Raises:
            InvalidCoordinatesError: If coordinates are out of valid range
            WeatherAPIError: If weather API request fails
        """
        self._validate_coordinates(lat, lon)
        return await self._provider.get_weather(lat, lon)

    def _validate_coordinates(self, lat: float, lon: float) -> None:
        """Validate coordinate ranges.
        
        Args:
            lat: Latitude to validate
            lon: Longitude to validate
            
        Raises:
            InvalidCoordinatesError: If coordinates are invalid
        """
        if not (-90 <= lat <= 90):
            raise InvalidCoordinatesError(
                f"Latitude must be between -90 and 90, got {lat}"
            )
        if not (-180 <= lon <= 180):
            raise InvalidCoordinatesError(
                f"Longitude must be between -180 and 180, got {lon}"
            )

