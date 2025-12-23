/**
 * Weather App Alpine.js Component
 * Main reactive component for weather dashboard
 */

function weatherApp() {
  return {
    weather: null,
    loading: false,
    error: null,
    cityInput: '',
    weatherIcon: 'sun',

    /**
     * Initialize component and detect location
     */
    async init() {
      await this.detectLocation();
      // Watch for weather changes to update icon
      this.$watch('weather', (newWeather) => {
        if (newWeather) {
          const newIcon = this.getWeatherIcon();
          console.log('Weather updated, icon:', newIcon, 'description:', newWeather.description);
          this.weatherIcon = newIcon;
          // Re-initialize icons after DOM update
          this.$nextTick(() => {
            setTimeout(() => {
              if (typeof lucide !== 'undefined') {
                lucide.createIcons();
              }
            }, 100);
          });
        }
      });
    },

    /**
     * Detect user's location and fetch weather
     */
    async detectLocation() {
      this.loading = true;
      this.error = null;
      
      try {
        const position = await WeatherAPI.getCurrentPosition();
        const { latitude, longitude } = position.coords;
        await this.fetchWeatherByCoordinates(latitude, longitude);
      } catch (error) {
        this.error = error.message;
        console.error('Location detection error:', error);
      } finally {
        this.loading = false;
      }
    },

    /**
     * Fetch weather by coordinates
     * @param {number} lat - Latitude
     * @param {number} lon - Longitude
     */
    async fetchWeatherByCoordinates(lat, lon) {
      this.loading = true;
      this.error = null;
      
      try {
        this.weather = await WeatherAPI.getWeatherByCoordinates(lat, lon);
        this.weatherIcon = this.getWeatherIcon();
        this.$nextTick(() => {
          if (typeof lucide !== 'undefined') {
            lucide.createIcons();
          }
        });
      } catch (error) {
        this.error = error.message || 'Failed to fetch weather data';
        console.error('Weather fetch error:', error);
      } finally {
        this.loading = false;
      }
    },

    /**
     * Fetch weather by city name
     * @param {string} city - City name
     */
    async fetchWeatherByCity(city) {
      if (!city || !city.trim()) {
        this.error = 'Please enter a city name';
        return;
      }

      this.loading = true;
      this.error = null;
      // Don't clear cityInput yet - keep it if there's an error so user can edit
      
      try {
        this.weather = await WeatherAPI.getWeatherByCity(city.trim());
        this.weatherIcon = this.getWeatherIcon();
        this.cityInput = ''; // Clear input only on success
        this.$nextTick(() => {
          if (typeof lucide !== 'undefined') {
            lucide.createIcons();
          }
        });
      } catch (error) {
        // Handle city not found specifically
        if (error.isCityNotFound) {
          this.error = `City "${error.city || city.trim()}" not found. Please check the spelling and try again.`;
        } else {
          this.error = error.message || 'Failed to fetch weather data';
        }
        console.error('Weather fetch error:', error);
        // Keep the city input so user can edit it
      } finally {
        this.loading = false;
      }
    },

    /**
     * Handle city search form submission
     */
    handleCitySearch() {
      const city = this.cityInput.trim();
      if (city) {
        this.fetchWeatherByCity(city);
      } else {
        this.error = 'Please enter a city name';
      }
    },

    /**
     * Determine weather CSS class based on conditions
     * Priority: Night → Cold → Rainy → Sunny (default)
     * @returns {string} Weather class name
     */
    getWeatherClass() {
      if (!this.weather) return 'weather-sunny';
      
      const temp = this.weather.temperature;
      const desc = this.weather.description.toLowerCase();
      const hour = new Date().getHours();
      
      // Night (6pm - 6am)
      if (hour < 6 || hour >= 18) return 'weather-night';
      
      // Cold/Snow (below 10°C or snow conditions)
      const coldKeywords = ['snow', 'sleet', 'ice', 'freezing', 'frost', 'blizzard'];
      if (temp < 10 || coldKeywords.some(k => desc.includes(k))) {
        return 'weather-cold';
      }
      
      // Rainy/Overcast
      const rainyKeywords = [
        'rain', 'drizzle', 'shower', 'downpour', 'precipitation',
        'cloud', 'cloudy', 'overcast', 'grey', 'gray',
        'mist', 'fog', 'haze', 'smoke', 'dust',
        'thunderstorm', 'storm', 'squall'
      ];
      if (rainyKeywords.some(k => desc.includes(k))) {
        return 'weather-rainy';
      }
      
      // Default: Sunny/Clear
      return 'weather-sunny';
    },

    /**
     * Get weather icon name for Lucide Icons
     * @returns {string} Icon name
     */
    getWeatherIcon() {
      if (!this.weather) return 'sun';
      
      const desc = this.weather.description.toLowerCase();
      const hour = new Date().getHours();
      const isNight = hour < 6 || hour >= 18;
      
      // Check in order of specificity (most specific first)
      
      // Thunderstorm (check before general rain)
      if (desc.includes('thunderstorm') || (desc.includes('storm') && !desc.includes('rain'))) {
        return 'cloud-lightning';
      }
      
      // Snow
      if (desc.includes('snow') || desc.includes('blizzard')) {
        return 'snowflake';
      }
      
      // Sleet/Ice
      if (desc.includes('sleet') || desc.includes('ice') || desc.includes('freezing')) {
        return 'cloud-snow';
      }
      
      // Heavy Rain (check before light rain)
      if (desc.includes('heavy') && desc.includes('rain')) {
        return 'cloud-rain-wind';
      }
      
      // Light Rain / Drizzle / Shower
      if (desc.includes('rain') || desc.includes('drizzle') || desc.includes('shower')) {
        return 'cloud-rain';
      }
      
      // Fog/Mist/Haze
      if (desc.includes('fog') || desc.includes('mist') || desc.includes('haze')) {
        return 'cloud-fog';
      }
      
      // Dust/Smoke/Sand
      if (desc.includes('dust') || desc.includes('smoke') || desc.includes('sand')) {
        return 'wind';
      }
      
      // Cloudy conditions (check before clear)
      if (desc.includes('cloud')) {
        return isNight ? 'cloud-moon' : 'cloud';
      }
      
      // Clear/Sunny/Fair conditions
      if (desc.includes('clear') || desc.includes('sunny') || desc.includes('fair')) {
        return isNight ? 'moon' : 'sun';
      }
      
      // Default: sun for day, moon for night
      return isNight ? 'moon' : 'sun';
    },

    /**
     * Get text color class based on weather
     * @returns {string} Text color class
     */
    getTextColorClass() {
      const weatherClass = this.getWeatherClass();
      return weatherClass === 'weather-night' ? 'text-white' : 'text-gray-800';
    },

    /**
     * Format temperature for display
     * @param {number} temp - Temperature in Celsius
     * @returns {string} Formatted temperature
     */
    formatTemperature(temp) {
      return `${Math.round(temp)}°C`;
    },
  };
}

