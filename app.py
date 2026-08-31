import streamlit as st
from services.geocoding import get_coordinates
from services.weather import get_weather_data
from utils.weather_codes import get_weather_info

# Set page configuration for a modern, wide layout
st.set_page_config(
    page_title="WeatherNow Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Adding custom CSS for cleaner styling
st.markdown("""
    <style>
        .weather-card {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .weather-header {
            text-align: center;
            padding-bottom: 20px;
        }
        .metric-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for default location
if 'lat' not in st.session_state:
    st.session_state.lat = 14.5995 # Manila default
if 'lon' not in st.session_state:
    st.session_state.lon = 120.9842
if 'location_name' not in st.session_state:
    st.session_state.location_name = "Manila, Philippines"

# Main Header
st.markdown("<div class='weather-header'><h1>🌤️ WeatherNow</h1><p>Simple, accurate weather information at a glance.</p></div>", unsafe_allow_html=True)

# Search Section layout
search_col, unit_col = st.columns([3, 1])

with search_col:
    # Use a form to handle search submission cleanly
    with st.form("search_form"):
        search_query = st.text_input("Search for a city or location...", placeholder="e.g., Tokyo, Japan")
        submit_search = st.form_submit_button("Search")

with unit_col:
    # Toggle for temperature units
    unit_toggle = st.radio("Temperature Unit", options=["Celsius (°C)", "Fahrenheit (°F)"], horizontal=True, label_visibility="collapsed")
    use_fahrenheit = "Fahrenheit" in unit_toggle

# Process search submission
if submit_search:
    if not search_query.strip():
        st.warning("Please enter a location to search.")
    else:
        with st.spinner("Searching for location..."):
            locations = get_coordinates(search_query)
            
            if not locations:
                st.error(f"Could not find location: '{search_query}'. Please try again with a different spelling or add the country name.")
            else:
                # If multiple locations, ideally we'd show a dropdown, but for simplicity we take the top result.
                # The geocoding API sorts by relevance.
                best_match = locations[0]
                st.session_state.lat = best_match['latitude']
                st.session_state.lon = best_match['longitude']
                
                # Construct a nice display name
                name_parts = [best_match.get('name')]
                if best_match.get('admin1'):
                    name_parts.append(best_match.get('admin1'))
                if best_match.get('country'):
                    name_parts.append(best_match.get('country'))
                
                st.session_state.location_name = ", ".join([p for p in name_parts if p])
                st.rerun()

# Fetch weather data for the current coordinates
with st.spinner("Fetching weather data..."):
    weather_data = get_weather_data(st.session_state.lat, st.session_state.lon, use_fahrenheit)

if weather_data:
    st.divider()
    
    # --- Current Weather Section ---
    current = weather_data['current']
    daily = weather_data['daily']
    
    # Get current weather icon and description
    weather_desc, weather_icon = get_weather_info(current['weather_code'])
    
    st.subheader(f"📍 {st.session_state.location_name}")
    
    # Use columns for a card-like layout
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown(f"<div class='weather-card' style='text-align: center;'>"
                    f"<h1 style='font-size: 4rem; margin: 0;'>{weather_icon}</h1>"
                    f"<h3>{weather_desc}</h3>"
                    f"</div>", unsafe_allow_html=True)
        
    with col2:
        unit_symbol = "°F" if use_fahrenheit else "°C"
        st.metric("Current Temperature", f"{current['temperature']}{unit_symbol}")
        st.metric("Feels Like", f"{current['apparent_temperature']}{unit_symbol}")
        
    with col3:
        st.metric("Humidity", f"{current['humidity']}%")
        st.metric("Wind Speed", f"{current['wind_speed']} km/h")
        if 'precipitation' in current:
             st.metric("Precipitation", f"{current['precipitation']} mm")

    st.divider()

    # --- Forecast Section ---
    st.subheader("📅 7-Day Forecast")
    
    # Create columns for daily forecast cards
    forecast_cols = st.columns(min(7, len(daily['time'])))
    
    for i, col in enumerate(forecast_cols):
        if i < len(daily['time']):
            date_str = daily['time'][i]
            
            # Formatting date to be more readable (e.g., "Mon, Aug 25")
            from datetime import datetime
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                display_date = date_obj.strftime("%a, %b %d")
            except ValueError:
                display_date = date_str

            day_code = daily['weather_code'][i]
            day_desc, day_icon = get_weather_info(day_code)
            
            max_temp = daily['temperature_2m_max'][i]
            min_temp = daily['temperature_2m_min'][i]
            precip_prob = daily.get('precipitation_probability_max', [0]*len(daily['time']))[i]

            with col:
                st.markdown(f"""
                <div class='weather-card' style='text-align: center; padding: 10px;'>
                    <strong>{display_date}</strong><br>
                    <span style='font-size: 2rem;'>{day_icon}</span><br>
                    <small>{day_desc}</small><br>
                    <hr style='margin: 5px 0;'>
                    <span style='color: #ff4b4b;'>H: {max_temp}°</span><br>
                    <span style='color: #4b8bff;'>L: {min_temp}°</span><br>
                    <small>🌧️ {precip_prob}%</small>
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()

    # --- Hourly Forecast Section (Next 24 hours) ---
    st.subheader("⏱️ Hourly Forecast (Next 24h)")
    
    hourly = weather_data['hourly']
    
    # We need to find the current time index to show the *next* 24 hours
    import datetime as dt
    now_iso = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:00")
    
    start_index = 0
    # Try to find the closest matching hour in the returned data
    for i, time_str in enumerate(hourly['time']):
        if time_str >= now_iso:
            start_index = i
            break
            
    end_index = min(start_index + 24, len(hourly['time']))
    
    # Create a horizontally scrollable container using columns or a chart
    # A chart is usually cleaner for hourly data in Streamlit
    import pandas as pd
    
    # Prepare data for the chart
    chart_data = pd.DataFrame({
        'Time': hourly['time'][start_index:end_index],
        'Temperature': hourly['temperature_2m'][start_index:end_index],
        'Precipitation Prob (%)': hourly.get('precipitation_probability', [0]*len(hourly['time']))[start_index:end_index]
    })
    
    # Format time for display
    chart_data['Time'] = pd.to_datetime(chart_data['Time']).dt.strftime('%I %p')
    
    # Display line chart for temperature
    st.line_chart(
        chart_data.set_index('Time')['Temperature'],
        use_container_width=True,
        color="#ffaa00"
    )
    
else:
    st.error("Failed to load weather data. The service might be temporarily unavailable. Please try again later.")