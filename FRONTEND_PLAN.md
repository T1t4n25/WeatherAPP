# Frontend Architecture Plan

## Overview
Alpine.js + Tailwind CSS frontend with adaptive dynamic color palette based on weather conditions.

---

## Directory Structure

```
static/
├── js/
│   ├── components/
│   │   └── weather-app.js      # Main Alpine.js component (weatherApp)
│   └── services/
│       └── weather-api.js      # API communication service
├── css/
│   └── custom.css              # Adaptive Dynamic Palette CSS
└── index.html                  # Main HTML entry point
```

---

## Component Design

### 1. Weather App Component (`weather-app.js`)
Alpine.js component with reactive state and weather logic.

**State:**
- `weather`: null | WeatherData
- `loading`: boolean
- `error`: null | string
- `cityInput`: string (for manual city search)

**Methods:**
- `init()`: Initialize component, detect location
- `detectLocation()`: Get user's geolocation via browser API
- `fetchWeatherByCoordinates(lat, lon)`: Fetch weather by coords
- `fetchWeatherByCity(city)`: Fetch weather by city name
- `getWeatherClass()`: Determine CSS class based on weather (Night → Cold → Rainy → Sunny)
- `getTextColorClass()`: Determine text color (white on dark, dark on light)
- `handleCitySearch()`: Handle city search form submission

**Weather Class Logic (Priority Order):**
1. **Night**: Hour < 6 || hour >= 18 → `weather-night`
2. **Cold/Snow**: temp < 10°C || description includes "snow" → `weather-cold`
3. **Rainy/Overcast**: description includes "rain"/"cloud"/"overcast" → `weather-rainy`
4. **Sunny/Clear** (default): → `weather-sunny`

---

### 2. Weather API Service (`weather-api.js`)
Service layer for API communication.

**Methods:**
- `async getWeatherByCoordinates(lat, lon)`: GET /api/v1/weather/current
- `async getWeatherByCity(city)`: POST /api/v1/weather/by-city
- `getCurrentPosition()`: Browser geolocation wrapper

**Error Handling:**
- Network errors → user-friendly messages
- API errors → show error message from response
- Location denied → show manual input option

---

### 3. Custom CSS (`custom.css`)
Adaptive Dynamic Palette with CSS variables and weather classes.

**CSS Variables:**
```css
--sunny-from: #FFBA52;
--sunny-to: #FF7A00;
--rainy-from: #748DA6;
--rainy-to: #9CB4CC;
--cold-from: #A0E7E5;
--cold-to: #B4F8C8;
--night-from: #2C3E50;
--night-to: #000000;
```

**Weather Classes:**
- `.weather-sunny`: Warm golden gradient
- `.weather-rainy`: Cool grey gradient
- `.weather-cold`: Icy mint gradient
- `.weather-night`: Dark gradient

**Features:**
- Smooth transitions (700ms)
- Text color adaptation
- Semi-transparent cards with backdrop blur

---

### 4. Index HTML (`index.html`)
Main HTML structure with Alpine.js and Tailwind CSS.

**Requirements:**
- Alpine.js CDN
- Tailwind CSS CDN
- Custom CSS link
- Weather app component initialization
- Responsive design (mobile-first)
- Loading states
- Error display
- City search input
- Weather data display

**Structure:**
```html
<div x-data="weatherApp()" :class="getWeatherClass()" class="min-h-screen transition-colors duration-700">
  <!-- Main container with dynamic background -->
  <div class="max-w-md mx-auto p-6">
    <!-- Weather card -->
    <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-8">
      <!-- Loading state -->
      <!-- Error state -->
      <!-- Weather display -->
      <!-- City search form -->
    </div>
  </div>
</div>
```

---

## UI/UX Design

### Layout
- **Centered card design** (max-width: md, centered)
- **Semi-transparent card** (bg-white/90 with backdrop-blur)
- **Rounded corners** (rounded-2xl)
- **Shadow** (shadow-xl)

### Weather Display
- **City name**: Large, bold heading
- **Temperature**: Extra large display (text-6xl or similar)
- **Description**: Weather description text
- **Details**: Humidity, wind speed (optional)
- **Icon**: Weather icon (emoji or icon)

### City Search
- **Input field**: Text input for city name
- **Submit button**: Search button
- **Debounce**: 300ms (optional, for better UX)

### States
- **Loading**: Spinner or loading text
- **Error**: Error message with retry option
- **Success**: Weather data display

---

## API Integration

### Endpoints Used
1. **GET /api/v1/weather/current?lat={lat}&lon={lon}**
   - Response: `{ data: WeatherData, timestamp: string }`

2. **POST /api/v1/weather/by-city**
   - Body: `{ city: string }`
   - Response: `{ data: WeatherData, timestamp: string }`

### Error Handling
- **422**: Invalid coordinates → Show error
- **404**: City not found → Show error
- **503**: API error → Show error
- **Network error**: Show network error message

---

## FastAPI Static Files Configuration

Add to `main.py`:
```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")
```

---

## Implementation Order

1. ✅ Plan frontend architecture
2. ⏭️ Create directory structure
3. ⏭️ Build CSS (custom.css)
4. ⏭️ Build API service (weather-api.js)
5. ⏭️ Build Alpine component (weather-app.js)
6. ⏭️ Build HTML (index.html)
7. ⏭️ Configure FastAPI static files
8. ⏭️ Test in browser

---

## Key Features

✅ **Adaptive Colors**: Background changes based on weather
✅ **Responsive Design**: Mobile-first with Tailwind
✅ **Location Detection**: Browser geolocation API
✅ **City Search**: Manual city input
✅ **Error Handling**: User-friendly error messages
✅ **Loading States**: Visual feedback during API calls
✅ **Smooth Transitions**: 700ms color transitions
✅ **Glanceability**: Instant visual weather understanding

---

## Browser Compatibility

- Chrome/Edge (modern)
- Firefox (modern)
- Safari (modern)
- Mobile browsers (iOS Safari, Chrome Mobile)

**Requirements:**
- Geolocation API support
- ES6+ JavaScript support
- CSS backdrop-filter support (optional, graceful degradation)

---

## Performance Considerations

- Alpine.js: 15KB gzipped (already lightweight)
- Tailwind CSS: CDN (development), consider build for production
- No build step required (Alpine.js works directly)
- Debounce city search (300ms)
- Lazy load weather icon (if using images)

---

**Status**: Ready for implementation! 🚀

