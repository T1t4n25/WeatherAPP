"""Domain exceptions for weather application."""


class WeatherAppException(Exception):
    """Base exception for weather app."""

    pass


class LocationNotFoundError(WeatherAppException):
    """Raised when location cannot be determined."""

    pass


class WeatherAPIError(WeatherAppException):
    """Raised when weather API request fails."""

    pass


class InvalidCoordinatesError(WeatherAppException):
    """Raised when coordinates are invalid."""

    pass

