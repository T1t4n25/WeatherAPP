"""OpenWeatherMap API client."""

import httpx

from src.domain.entities.weather import WeatherData
from src.domain.exceptions import InvalidCoordinatesError, WeatherAPIError
from src.domain.interfaces.weather_provider import WeatherProvider
from src.infrastructure.config.settings import Settings


class OpenWeatherMapClient:
    """OpenWeatherMap API client implementing WeatherProvider."""

    BASE_URL = "https://api.openweathermap.org/data/2.5"
    GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"

    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None):
        """Initialize OpenWeatherMap client.
        
        Args:
            settings: Application settings containing API key
            client: Optional httpx client (for testing or reuse)
        """
        self._api_key = settings.openweather_api_key
        self._client = client or httpx.AsyncClient(timeout=10.0)

    async def get_weather(self, lat: float, lon: float) -> WeatherData:
        """Fetch weather data for given coordinates.
        
        Args:
            lat: Latitude in decimal degrees
            lon: Longitude in decimal degrees
            
        Returns:
            WeatherData object with current weather
            
        Raises:
            WeatherAPIError: If API request fails
            InvalidCoordinatesError: If coordinates are invalid
        """
        try:
            response = await self._client.get(
                f"{self.BASE_URL}/weather",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self._api_key,
                    "units": "metric",
                },
            )
            response.raise_for_status()
            data = response.json()

            return WeatherData(
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                description=data["weather"][0]["description"],
                city=data["name"],
                lat=data["coord"]["lat"],
                lon=data["coord"]["lon"],
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                raise InvalidCoordinatesError(
                    f"Invalid coordinates: lat={lat}, lon={lon}"
                ) from e
            raise WeatherAPIError(f"Weather API error: {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise WeatherAPIError(f"Failed to connect to weather API: {str(e)}") from e
        except (KeyError, IndexError) as e:
            raise WeatherAPIError(f"Unexpected API response format: {str(e)}") from e

    async def get_coordinates_by_city(self, city: str) -> tuple[float, float]:
        """Get coordinates for a city using geocoding API.
        
        Args:
            city: City name
            
        Returns:
            Tuple of (latitude, longitude)
            
        Raises:
            WeatherAPIError: If geocoding fails or city not found
        """
        try:
            response = await self._client.get(
                self.GEOCODING_URL,
                params={"q": city, "appid": self._api_key, "limit": 1},
            )
            response.raise_for_status()
            data = response.json()

            if not data or len(data) == 0:
                raise WeatherAPIError(f"City not found: {city}")

            location = data[0]
            return (location["lat"], location["lon"])
        except httpx.HTTPStatusError as e:
            raise WeatherAPIError(
                f"Geocoding API error: {e.response.status_code}"
            ) from e
        except httpx.RequestError as e:
            raise WeatherAPIError(
                f"Failed to connect to geocoding API: {str(e)}"
            ) from e
        except (KeyError, IndexError) as e:
            raise WeatherAPIError(f"Unexpected geocoding response format: {str(e)}") from e

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

