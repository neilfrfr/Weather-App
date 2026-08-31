# WeatherNow 🌤️

A simple, clean, and accurate weather dashboard built with Python. 

This application allows users to search for locations worldwide and instantly view current weather conditions, hourly breakdowns, and multi-day forecasts. It is designed to be beginner-friendly but structured well enough for real-world use.

## Features

* **Location Search:** Find the weather for almost any city in the world.
* **Current Weather:** See temperature, "feels-like" temperature, humidity, and wind speed at a glance.
* **Detailed Forecasts:** View hourly updates for the rest of the day and a multi-day outlook.
* **Unit Toggle:** Easily switch between Celsius and Fahrenheit.
* **Smart Error Handling:** Helpful messages if a location isn't found or if the internet connection drops, rather than crashing.

## Tools Used

* **Python:** The core programming language.
* **Streamlit:** Used to build the web interface quickly and cleanly.
* **Open-Meteo API:** Provides the weather and location data for free (no API key required).
* **Requests:** Helps the application talk to the internet to fetch the weather data.

## Folder Structure

```text
weather-app/
│
├── app.py                  # Main application and web interface
├── requirements.txt        # List of required Python tools
├── README.md               # Project instructions
├── .gitignore              # Tells Git which files to ignore
│
├── services/               # Talks to the internet
│   ├── __init__.py
│   ├── geocoding.py        # Handles the city search
│   └── weather.py          # Handles getting the weather data
│
└── utils/                  # Helper tools
    ├── __init__.py
    └── weather_codes.py    # Turns number codes into readable text and emojis