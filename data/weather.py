import requests


def get_weather_and_aqi(lat, lon):
    """Fetches current weather and Air Quality using the reliable 'current' endpoint."""
    try:
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,apparent_temperature,weather_code,wind_speed_10m"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        current_weather = weather_response.json().get("current", {})

        aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi,pm2_5"
        aqi_response = requests.get(aqi_url)
        aqi_response.raise_for_status()
        current_aqi = aqi_response.json().get("current", {})

        if not current_weather or not current_aqi:
            print("Warning: Received empty data from Open-Meteo.")
            return None, None

        return current_weather, current_aqi

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not fetch weather/AQI data. Reason: {e}")
        return None, None