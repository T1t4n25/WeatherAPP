"""Location response DTO."""

from datetime import datetime

from pydantic import BaseModel, Field


class LocationData(BaseModel):
    """Location data model.
    
    Attributes:
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
        city: City name (optional)
    """

    lat: float
    lon: float
    city: str | None = None


class LocationResponse(BaseModel):
    """Location API response DTO.
    
    Attributes:
        data: Location data
        timestamp: Response timestamp in ISO format
    """

    data: LocationData
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""

        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z",
        }

