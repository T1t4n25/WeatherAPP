# Project Context for AI Agents

## Quick Overview

Weather Dashboard app with FastAPI backend and Alpine.js frontend. Implements adaptive color system that changes background based on weather conditions.

## Key Architecture Decisions

### Backend
- **Clean Architecture** with three layers: Domain → Application → Infrastructure
- **SOLID Principles** throughout
- **Protocol-based interfaces** (Python typing.Protocol)
- **Absolute imports** from `src` (e.g., `from src.domain.entities.weather import WeatherData`)
- **Serverless-ready**: Stateless, env vars only, `@lru_cache()` for singletons

### Frontend
- **Alpine.js** for reactivity (15KB, no build step)
- **Tailwind CSS** via CDN
- **Lucide Icons** for weather icons
- **Adaptive colors**: Background changes via `weatherClass` reactive property

## Important Files

- `.cursorrules` - Complete development rules and standards
- `src/main.py` - FastAPI app entry, serves static files
- `static/js/components/weather-app.js` - Main Alpine.js component
- `static/css/custom.css` - Adaptive color palette CSS

## Critical Implementation Details

### Weather Class Logic (Priority Order)
1. **Night** (6pm - 6am) → `weather-night`
2. **Cold** (temp < 10°C OR snow keywords) → `weather-cold`
3. **Rainy** (rain/cloud keywords) → `weather-rainy`
4. **Sunny** (default) → `weather-sunny`

### Reactive Properties
- `weatherClass` - Background CSS class (must update when weather changes)
- `weatherIcon` - Lucide icon name (must update when weather changes)
- Both updated in `$watch('weather')` and after fetching weather

### API Endpoints
- `GET /api/v1/weather/current?lat={lat}&lon={lon}`
- `POST /api/v1/weather/by-city` (body: `{"city": "London"}`)

### Error Handling
- City not found: 404 status with `isCityNotFound` flag in frontend
- Network errors: User-friendly messages
- Location denied: Falls back to city search

## Current Status

✅ Backend fully implemented  
✅ Frontend fully implemented  
✅ Mobile-responsive  
✅ Error handling complete  
✅ Icons and colors working  

## Development Commands

```bash
# Run server
uvicorn src.main:app --reload --port 8000

# Install deps
pip install -r requirements.txt
```

## Notes for Agents

- All imports use absolute paths from `src`
- Frontend uses reactive properties, not method calls in bindings
- Icons require `lucide.createIcons()` after DOM updates
- Weather class must be stored as property for Alpine reactivity

