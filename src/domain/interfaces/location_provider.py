"""Location provider interface."""

from typing import Protocol


class LocationProvider(Protocol):
    """Protocol for location detection providers."""

    async def get_location(self) -> tuple[float, float]:
        """Get current location coordinates.
        
        Returns:
            Tuple of (latitude, longitude) in decimal degrees
            
        Raises:
            LocationNotFoundError: If location cannot be determined
        """
        ...

