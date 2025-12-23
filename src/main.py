"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routers
app.include_router(api_router)


@app.get("/")
async def root():
    """Root endpoint - serves the frontend HTML.
    
    Returns:
        Frontend HTML file
    """
    return FileResponse("static/index.html")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint.
    
    Returns:
        Health status
    """
    return {"status": "healthy"}

