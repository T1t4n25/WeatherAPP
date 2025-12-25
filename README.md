# Weather Dashboard

A modern weather dashboard application built with FastAPI backend and Alpine.js frontend, featuring adaptive color palettes that change based on weather conditions for instant visual understanding.

## Features

- 🌍 **Automatic Location Detection** - Uses browser geolocation API
- 🔍 **City Search** - Search for weather by city name
- 🎨 **Adaptive Color System** - Background colors change based on weather conditions:
  - ☀️ Sunny/Clear: Warm golden gradient
  - 🌧️ Rainy/Overcast: Cool grey gradient
  - ❄️ Cold/Snow: Icy mint gradient
  - 🌙 Night: Dark gradient
- 📱 **Mobile-Friendly** - Responsive design optimized for all screen sizes
- ⚡ **Fast & Lightweight** - Alpine.js (15KB) + Tailwind CSS
- 🎯 **Weather Icons** - Dynamic Lucide icons based on conditions

## Tech Stack

### Backend
- **Python 3.13+**
- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **OpenWeatherMap API** - Weather data source

### Frontend
- **Alpine.js** - Lightweight reactive framework (15KB)
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide Icons** - Beautiful icon library

## Architecture

### Backend Structure (Simplified)
```
src/
├── models.py           # Data models (WeatherData, WeatherResponse)
├── config.py           # Configuration and settings
├── service.py          # Weather service (API client + business logic)
├── routes.py           # API routes
└── main.py             # Application entry point
```

### Frontend Structure
```
static/
├── js/
│   ├── components/      # Alpine.js components
│   └── services/        # API communication
├── css/
│   └── custom.css       # Adaptive color system
└── index.html           # Main HTML
```

## Getting Started

### Prerequisites

- Python 3.13 or higher (for local development)
- Docker and Docker Compose (optional, for containerized deployment)
- OpenWeatherMap API key ([Get one here](https://openweathermap.org/api))

### Option 1: Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd WeatherAPP
   ```

2. **Create `.env` file**
   ```bash
   cp env.example .env
   ```
   Edit `.env` and add your OpenWeatherMap API key:
   ```bash
   OPENWEATHER_API_KEY=your_api_key_here
   ENVIRONMENT=production
   CACHE_TTL=300
   ```

3. **Build and run with Docker**

   **Option A: Using Docker directly**
   ```bash
   # Build the Docker image
   docker build -t weather-dashboard .
   
   # Run the container
   docker run -d -p 8000:8000 --env-file .env --name weather-app weather-dashboard
   ```

   **Option B: Using Docker Compose (Recommended)**
   ```bash
   docker-compose up -d
   ```

4. **Open in browser**
   ```
   http://localhost:8000
   ```

### Option 2: Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd WeatherAPP
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   ```
   Edit `.env` and add your OpenWeatherMap API key:
   ```bash
   OPENWEATHER_API_KEY=your_api_key_here
   ENVIRONMENT=development
   CACHE_TTL=300
   ```

4. **Run the development server**
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

5. **Open in browser**
   ```
   http://localhost:8000
   ```

## API Endpoints

### GET /api/v1/weather/current
Get current weather by coordinates.

**Query Parameters:**
- `lat` (float, required): Latitude
- `lon` (float, required): Longitude

**Response:**
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
Get current weather by city name.

**Request Body:**
```json
{
  "city": "London"
}
```

**Response:** Same format as above

### GET /health
Health check endpoint.

## Project Structure

```
WeatherAPP/
├── src/                    # Backend source code
│   ├── models.py          # Data models (WeatherData, WeatherResponse)
│   ├── config.py          # Configuration and settings
│   ├── service.py         # Weather service (API client + business logic)
│   ├── routes.py          # API routes
│   └── main.py           # FastAPI app entry point
├── static/               # Frontend files
│   ├── js/              # JavaScript components and services
│   ├── css/             # Custom CSS
│   └── index.html       # Main HTML file
├── .cursorrules         # Development rules and standards
├── requirements.txt     # Python dependencies
├── env.example          # Environment variables template
├── Dockerfile           # Docker container configuration
├── docker-compose.yml   # Docker Compose configuration
├── .dockerignore        # Docker ignore file
└── README.md           # This file
```

## Design Philosophy

### Adaptive Dynamic Palette

The app uses an **adaptive color system** that changes the background based on weather conditions for instant visual understanding:

| Condition | Colors | Logic |
|-----------|--------|-------|
| Clear/Sunny | `#FFBA52 → #FF7A00` | Default (warm/golden) |
| Rainy/Overcast | `#748DA6 → #9CB4CC` | Contains: rain, cloud, overcast, mist, fog |
| Cold/Snow | `#A0E7E5 → #B4F8C8` | Temp < 10°C OR contains: snow, sleet, ice |
| Night | `#2C3E50 → #000000` | 6pm - 6am (dark) |

**Priority Order:** Night → Cold → Rainy → Sunny (default)

## Development

### Code Standards

- **Backend**: Simple, straightforward structure (no over-engineering)
- **Type Hints**: Used where helpful
- **Async I/O**: All I/O operations are async
- **Error Handling**: Simple error handling using HTTPException and standard exceptions
- **Frontend**: Alpine.js reactive components, Tailwind CSS utilities

### Testing

The project follows a minimal testing strategy focusing on critical paths:

```bash
# Run tests (if implemented)
pytest tests/
```

### Serverless Deployment

The application is serverless-ready and can be deployed to:
- AWS Lambda
- Vercel
- Railway
- Google Cloud Run

**Key Requirements:**
- All secrets in environment variables
- Stateless handlers
- No file system writes
- Connection pooling with cleanup

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Yes |
| `ENVIRONMENT` | Environment name (development/production) | No |
| `CACHE_TTL` | Cache TTL in seconds (default: 300) | No |

## License

This project is open source and available for personal and commercial use.

## Credits

- Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
- Icons by [Lucide](https://lucide.dev/)
- Built with [FastAPI](https://fastapi.tiangolo.com/) and [Alpine.js](https://alpinejs.dev/)

