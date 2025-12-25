"""Data models for weather API."""

from datetime import datetime

from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    """Weather data model."""
    temperature: float
    humidity: int
    wind_speed: float
    description: str
    city: str
    lat: float
    lon: float


class WeatherResponse(BaseModel):
    """Weather API response model."""
    data: WeatherData
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z",
        }

