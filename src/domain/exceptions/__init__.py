"""Domain-specific exceptions."""

from .weather_exceptions import (
    InvalidCoordinatesError,
    LocationNotFoundError,
    WeatherAPIError,
    WeatherAppException,
)

__all__ = [
    "WeatherAppException",
    "LocationNotFoundError",
    "WeatherAPIError",
    "InvalidCoordinatesError",
]

