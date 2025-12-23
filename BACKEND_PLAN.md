# Backend Architecture Plan

## Overview
FastAPI backend for Weather Dashboard following Clean Architecture + Hexagonal Architecture principles.

---

## Directory Structure

```
src/
├── domain/                    # Business logic & entities (no dependencies)
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── weather.py        # WeatherData entity
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── weather_exceptions.py  # Domain exceptions
│   └── interfaces/
│       ├── __init__.py
│       ├── weather_provider.py    # WeatherProvider Protocol
│       └── location_provider.py   # LocationProvider Protocol
├── application/
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── weather_service.py     # Business logic
│   └── dto/
│       ├── __init__.py
│       ├── weather_dto.py         # WeatherResponse DTO
│       └── location_dto.py        # LocationResponse DTO
├── infrastructure/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── weather.py         # Weather endpoints
│   │   │   └── location.py        # Location endpoints
│   │   └── dependencies.py        # FastAPI dependencies
│   ├── external/
│   │   ├── __init__.py
│   │   └── openweather_client.py  # OpenWeatherMap API client
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py            # Pydantic Settings
│   └── middleware/
│       ├── __init__.py
│       └── error_handler.py       # Exception handlers
└── main.py                         # FastAPI app entry point
```

---

## Layer Breakdown

### 1. Domain Layer (No External Dependencies)

#### Entities
- **WeatherData** (dataclass)
  - temperature: float
  - humidity: int
  - wind_speed: float
  - description: str
  - city: str
  - lat: float
  - lon: float

#### Exceptions
- **WeatherAppException** (base)
- **LocationNotFoundError**
- **WeatherAPIError**
- **InvalidCoordinatesError**

#### Interfaces (Protocols)
- **WeatherProvider**
  - `async def get_weather(lat: float, lon: float) -> WeatherData`
- **LocationProvider** (future: GPS, IP-based)
  - `async def get_location() -> tuple[float, float]`

---

### 2. Application Layer (Depends on Domain Only)

#### Services
- **WeatherService**
  - Depends on: WeatherProvider (interface)
  - Methods:
    - `async def get_weather_by_coordinates(lat, lon) -> WeatherData`
    - `async def get_weather_by_city(city: str) -> WeatherData` (uses geocoding)

#### DTOs (Pydantic Models)
- **WeatherResponse**
  - data: WeatherData
  - timestamp: datetime
- **LocationResponse**
  - data: dict (lat, lon, city)
  - timestamp: datetime

---

### 3. Infrastructure Layer (External Concerns)

#### Configuration
- **Settings** (Pydantic BaseSettings)
  - openweather_api_key: str
  - environment: str = "development"
  - cache_ttl: int = 300
  - `@lru_cache() get_settings() -> Settings`

#### External API Client
- **OpenWeatherMapClient** (implements WeatherProvider)
  - Uses httpx.AsyncClient
  - Methods:
    - `async def get_weather(lat, lon) -> WeatherData`
    - `async def get_coordinates_by_city(city: str) -> tuple[float, float]`
  - Error handling for API failures

#### API Routes
- **Weather Routes** (`/api/v1/weather/`)
  - `GET /current?lat={lat}&lon={lon}` -> WeatherResponse
  - `POST /by-city` (body: {"city": "London"}) -> WeatherResponse
- **Location Routes** (`/api/v1/location/`)
  - `GET /detect` -> LocationResponse (future implementation)

#### Middleware
- CORS middleware (allow localhost for development)
- Exception handlers:
  - LocationNotFoundError -> 404
  - WeatherAPIError -> 503
  - ValidationError -> 422
  - Generic -> 500

#### Dependencies
- `get_weather_service()` -> WeatherService (with injected OpenWeatherMapClient)
- `get_settings()` -> Settings

---

### 4. Main Entry Point

#### main.py
- Create FastAPI app
- Include routers
- Add middleware (CORS, error handlers)
- Root endpoint for health check

---

## API Endpoints Specification

### GET /api/v1/weather/current
**Query Parameters:**
- lat: float (required)
- lon: float (required)

**Response (200 OK):**
```json
{
  "data": {
    "temperature": 22.5,
    "humidity": 65,
    "wind_speed": 3.2,
    "description": "Partly cloudy",
    "city": "London",
    "lat": 51.5074,
    "lon": -0.1278
  },
  "timestamp": "2024-01-20T10:30:00Z"
}
```

### POST /api/v1/weather/by-city
**Request Body:**
```json
{
  "city": "London"
}
```

**Response (200 OK):** Same format as above

### GET /api/v1/location/detect
**Response (200 OK):**
```json
{
  "data": {
    "lat": 51.5074,
    "lon": -0.1278,
    "city": "London"
  },
  "timestamp": "2024-01-20T10:30:00Z"
}
```

---

## Implementation Order

1. ✅ Domain Layer: Entities, Exceptions, Interfaces
2. ✅ Application Layer: DTOs, Services
3. ✅ Infrastructure: Config, External Client
4. ✅ Infrastructure: API Routes, Middleware
5. ✅ Main entry point
6. ✅ Supporting files (requirements.txt, .env.example, .gitignore)

---

## Key Design Decisions

1. **Protocols over ABC**: Use `typing.Protocol` for interfaces (structural subtyping)
2. **Pydantic for DTOs**: FastAPI integration + validation
3. **httpx.AsyncClient**: Async HTTP client with connection pooling
4. **Dependency Injection**: FastAPI's `Depends()` for clean DI
5. **Error Handling**: Domain exceptions -> HTTP status codes
6. **Type Hints**: Mandatory for all functions
7. **Serverless-Ready**: Stateless, env vars only, `@lru_cache()` for settings

---

## OpenWeatherMap API Integration

- Base URL: `https://api.openweathermap.org/data/2.5/weather`
- Endpoints used:
  - Current weather by coordinates: `?lat={lat}&lon={lon}&appid={key}&units=metric`
  - Geocoding (city -> coords): `https://api.openweathermap.org/geo/1.0/direct?q={city}&appid={key}`

---

## Next Steps After Backend

1. Frontend (Alpine.js + Tailwind CSS)
2. Tests (minimal - critical paths only)
3. Documentation (README.md)
4. Deployment configuration (serverless)

