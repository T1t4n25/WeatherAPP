"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.api.routes import api_router
from src.infrastructure.middleware.error_handler import setup_exception_handlers

app = FastAPI(
    title="Weather Dashboard API",
    description="Weather dashboard API with OpenWeatherMap integration",
    version="1.0.0",
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup exception handlers
setup_exception_handlers(app)

# Include API routers
app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint for health check.
    
    Returns:
        Simple health check response
    """
    return {"message": "Weather Dashboard API", "status": "running"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint.
    
    Returns:
        Health status
    """
    return {"status": "healthy"}

