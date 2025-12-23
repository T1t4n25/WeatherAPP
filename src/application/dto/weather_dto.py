"""Weather response DTO."""

from datetime import datetime

from pydantic import BaseModel, Field

from src.domain.entities.weather import WeatherData


class WeatherResponse(BaseModel):
    """Weather API response DTO.
    
    Attributes:
        data: Weather data entity
        timestamp: Response timestamp in ISO format
    """

    data: WeatherData
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""

        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z",
        }

