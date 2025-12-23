"""Domain interfaces (Protocols)."""

from .location_provider import LocationProvider
from .weather_provider import WeatherProvider

__all__ = ["WeatherProvider", "LocationProvider"]

