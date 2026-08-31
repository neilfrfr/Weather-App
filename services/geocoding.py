import requests
import streamlit as st
import logging

# Configure basic logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@st.cache_data(ttl=3600) # Cache results for 1 hour to reduce API calls
def get_coordinates(query: str, count: int = 5) -> list:
    """
    Search for a location using the Open-Meteo Geocoding API.
    
    Args:
        query (str): The name of the city/location to search for.
        count (int): The maximum number of results to return.
        
    Returns:
        list: A list of dictionaries containing location details 
              (latitude, longitude, name, country, etc.)
              Returns an empty list if no results or if an error occurs.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    
    params = {
        "name": query,
        "count": count,
        "language": "en",
        "format": "json"
    }
    
    try:
        # Include a timeout to prevent hanging if the API is down
        response = requests.get(url, params=params, timeout=10)
        
        # Raise an exception for bad HTTP status codes (4xx or 5xx)
        response.raise_for_status()
        
        data = response.json()
        
        # The API returns a 'results' key if locations are found
        if "results" in data:
            return data["results"]
        else:
            return []
            
    except requests.exceptions.Timeout:
        logger.error(f"Geocoding API timeout when searching for '{query}'")
        st.toast("Location search timed out. Please check your connection.", icon="⚠️")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Geocoding API error: {e}")
        # We don't want to crash the app, just return empty and let the UI handle it
        return []
    except Exception as e:
        logger.error(f"Unexpected error in geocoding: {e}")
        return []