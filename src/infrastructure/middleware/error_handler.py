"""Exception handlers for FastAPI."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions import (
    InvalidCoordinatesError,
    LocationNotFoundError,
    WeatherAPIError,
    WeatherAppException,
)


def setup_exception_handlers(app: FastAPI) -> None:
    """Setup exception handlers for the FastAPI app.
    
    Args:
        app: FastAPI application instance
    """

    @app.exception_handler(LocationNotFoundError)
    async def location_not_found_handler(
        request: Request, exc: LocationNotFoundError
    ) -> JSONResponse:
        """Handle location not found errors."""
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "location_not_found", "message": str(exc)},
        )

    @app.exception_handler(WeatherAPIError)
    async def weather_api_error_handler(
        request: Request, exc: WeatherAPIError
    ) -> JSONResponse:
        """Handle weather API errors."""
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"error": "weather_api_error", "message": str(exc)},
        )

    @app.exception_handler(InvalidCoordinatesError)
    async def invalid_coordinates_handler(
        request: Request, exc: InvalidCoordinatesError
    ) -> JSONResponse:
        """Handle invalid coordinates errors."""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "invalid_coordinates", "message": str(exc)},
        )

    @app.exception_handler(WeatherAppException)
    async def weather_app_exception_handler(
        request: Request, exc: WeatherAppException
    ) -> JSONResponse:
        """Handle general weather app exceptions."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "weather_app_error", "message": str(exc)},
        )

