/**
 * Weather API Service
 * Handles all API communication for weather data
 */

const WeatherAPI = {
  /**
   * Get current weather by coordinates
   * @param {number} lat - Latitude
   * @param {number} lon - Longitude
   * @returns {Promise<Object>} Weather data
   */
  async getWeatherByCoordinates(lat, lon) {
    const response = await fetch(
      `/api/v1/weather/current?lat=${lat}&lon=${lon}`
    );
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data.data;
  },

  /**
   * Get current weather by city name
   * @param {string} city - City name
   * @returns {Promise<Object>} Weather data
   */
  async getWeatherByCity(city) {
    const response = await fetch('/api/v1/weather/by-city', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ city }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data.data;
  },

  /**
   * Get current position using browser geolocation API
   * @returns {Promise<GeolocationPosition>} Geolocation position
   */
  getCurrentPosition() {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation is not supported by your browser'));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => resolve(position),
        (error) => {
          let message = 'Could not detect location';
          switch (error.code) {
            case error.PERMISSION_DENIED:
              message = 'Location access denied. Please search for a city instead.';
              break;
            case error.POSITION_UNAVAILABLE:
              message = 'Location information unavailable. Please search for a city.';
              break;
            case error.TIMEOUT:
              message = 'Location request timed out. Please search for a city instead.';
              break;
          }
          reject(new Error(message));
        },
        {
          enableHighAccuracy: false, // Use less accurate but faster location
          timeout: 15000, // 15 seconds timeout
          maximumAge: 300000, // Accept cached location up to 5 minutes old
        }
      );
    });
  },
};

