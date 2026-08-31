import requests
import streamlit as st
import logging

logger = logging.getLogger(__name__)

@st.cache_data(ttl=900) # Cache for 15 minutes to avoid hitting rate limits
def get_weather_data(lat: float, lon: float, use_fahrenheit: bool = False) -> dict:
    """
    Fetch weather data for given coordinates using the Open-Meteo Weather API.
    
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        use_fahrenheit (bool): If True, requests temperature in Fahrenheit. Default is Celsius.
        
    Returns:
        dict: A dictionary containing current, hourly, and daily weather data.
              Returns None if the request fails.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    
    # Setting up the parameters for the API call
    params = {
        "latitude": lat,
        "longitude": lon,
        # Request current weather variables
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
        # Request hourly forecast for the next few days
        "hourly": "temperature_2m,precipitation_probability,weather_code",
        # Request daily forecast
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        # Automatically detect timezone based on coordinates
        "timezone": "auto"
    }
    
    # Adjust units if requested
    if use_fahrenheit:
        params["temperature_unit"] = "fahrenheit"
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Restructure the data slightly for easier use in the UI
        parsed_data = {
            "current": {
                "temperature": data.get("current", {}).get("temperature_2m"),
                "humidity": data.get("current", {}).get("relative_humidity_2m"),
                "apparent_temperature": data.get("current", {}).get("apparent_temperature"),
                "precipitation": data.get("current", {}).get("precipitation"),
                "weather_code": data.get("current", {}).get("weather_code"),
                "wind_speed": data.get("current", {}).get("wind_speed_10m"),
                "time": data.get("current", {}).get("time")
            },
            "hourly": data.get("hourly", {}),
            "daily": data.get("daily", {})
        }
        
        return parsed_data
        
    except requests.exceptions.Timeout:
        logger.error("Weather API timeout.")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Weather API request error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error formatting weather data: {e}")
        return None