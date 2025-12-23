"""Application settings using Pydantic BaseSettings."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    Attributes:
        openweather_api_key: OpenWeatherMap API key
        environment: Environment name (development, production)
        cache_ttl: Cache TTL in seconds (default: 300 = 5 minutes)
    """

    openweather_api_key: str
    environment: str = "development"
    cache_ttl: int = 300

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (singleton pattern).
    
    Returns:
        Settings instance (cached)
    """
    return Settings()

