"""API routes."""

from fastapi import APIRouter

from src.infrastructure.api.routes.location import router as location_router
from src.infrastructure.api.routes.weather import router as weather_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(weather_router, prefix="/weather", tags=["weather"])
api_router.include_router(location_router, prefix="/location", tags=["location"])

__all__ = ["api_router"]

