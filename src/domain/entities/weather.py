"""Weather entity representing core weather data."""

from dataclasses import dataclass


@dataclass
class WeatherData:
    """Core weather data entity.
    
    Attributes:
        temperature: Temperature in Celsius
        humidity: Humidity percentage (0-100)
        wind_speed: Wind speed in m/s
        description: Weather description (e.g., "Clear sky")
        city: City name
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
    """

    temperature: float
    humidity: int
    wind_speed: float
    description: str
    city: str
    lat: float
    lon: float

