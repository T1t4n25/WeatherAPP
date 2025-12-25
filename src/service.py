"""Weather service for fetching weather data."""

import httpx

from src.config import Settings, get_settings
from src.models import WeatherData


class WeatherService:
    """Service for fetching weather data from OpenWeatherMap."""

    BASE_URL = "https://api.openweathermap.org/data/2.5"
    GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"

    def __init__(self, settings: Settings | None = None):
        """Initialize weather service."""
        self._settings = settings or get_settings()
        self._client = httpx.AsyncClient(timeout=10.0)

    async def get_weather_by_coordinates(self, lat: float, lon: float) -> WeatherData:
        """Get weather data by coordinates."""
        # Validate coordinates
        if not (-90 <= lat <= 90):
            raise ValueError(f"Latitude must be between -90 and 90, got {lat}")
        if not (-180 <= lon <= 180):
            raise ValueError(f"Longitude must be between -180 and 180, got {lon}")

        try:
            response = await self._client.get(
                f"{self.BASE_URL}/weather",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self._settings.openweather_api_key,
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
                raise ValueError(f"Invalid coordinates: lat={lat}, lon={lon}") from e
            raise RuntimeError(f"Weather API error: {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise RuntimeError(f"Failed to connect to weather API: {str(e)}") from e
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Unexpected API response format: {str(e)}") from e

    async def get_weather_by_city(self, city: str) -> WeatherData:
        """Get weather data by city name."""
        try:
            # Get coordinates
            response = await self._client.get(
                self.GEOCODING_URL,
                params={"q": city, "appid": self._settings.openweather_api_key, "limit": 1},
            )
            response.raise_for_status()
            data = response.json()

            if not data or len(data) == 0:
                raise ValueError(f"City not found: {city}")

            location = data[0]
            lat, lon = location["lat"], location["lon"]

            # Get weather by coordinates
            return await self.get_weather_by_coordinates(lat, lon)
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Geocoding API error: {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise RuntimeError(f"Failed to connect to geocoding API: {str(e)}") from e
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Unexpected geocoding response format: {str(e)}") from e
        except ValueError as e:
            # Re-raise ValueError (city not found or invalid coords)
            raise

