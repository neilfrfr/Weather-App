"""
Utility file to convert Open-Meteo WMO weather codes into
human-readable descriptions and emojis.
Reference: https://open-meteo.com/en/docs
"""

# Dictionary mapping WMO codes to a tuple of (Description, Emoji)
WEATHER_CODES = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Depositing rime fog", "🌫️"),
    51: ("Light drizzle", "🌧️"),
    53: ("Moderate drizzle", "🌧️"),
    55: ("Dense drizzle", "🌧️"),
    56: ("Light freezing drizzle", "🌧️❄️"),
    57: ("Dense freezing drizzle", "🌧️❄️"),
    61: ("Slight rain", "☔"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    66: ("Light freezing rain", "🌧️❄️"),
    67: ("Heavy freezing rain", "🌧️❄️"),
    71: ("Slight snow fall", "🌨️"),
    73: ("Moderate snow fall", "❄️"),
    75: ("Heavy snow fall", "❄️"),
    77: ("Snow grains", "❄️"),
    80: ("Slight rain showers", "🌦️"),
    81: ("Moderate rain showers", "🌧️"),
    82: ("Violent rain showers", "🌧️"),
    85: ("Slight snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with slight hail", "⛈️🧊"),
    99: ("Thunderstorm with heavy hail", "⛈️🧊"),
}

def get_weather_info(code: int) -> tuple[str, str]:
    """
    Get the description and emoji for a given WMO weather code.
    
    Args:
        code (int): The WMO weather code returned by the API.
        
    Returns:
        tuple[str, str]: A tuple containing the (Description, Emoji).
                         Returns a default unknown value if code is not found.
    """
    # Return the mapped value, or a generic fallback if the code is unknown
    return WEATHER_CODES.get(code, ("Unknown conditions", "❓"))