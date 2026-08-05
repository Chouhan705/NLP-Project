from config import API_KEYS, WMO_CODES
from location import get_device_location
from weather import get_weather_and_aqi
from traffic import get_traffic_info
from news import get_news_headlines
from health import generate_health_report


def main():
    # Get the location when the script starts
    location = get_device_location()

    print(f"\n{'='*50}")
    print(f"   DAILY BRIEFING FOR {location['city'].upper()} ")
    print(f"{'='*50}\n")

    # Fetch Weather and AQI
    weather, aqi = get_weather_and_aqi(location["lat"], location["lon"])
    if weather and aqi:
        weather_desc = WMO_CODES.get(weather.get('weather_code', -1), "Unknown Condition")
        print(f"--- ⛅ Weather & Air Quality ---")
        print(f"Temperature: {weather.get('temperature_2m')}°C (Feels like {weather.get('apparent_temperature')}°C)")
        print(f"Condition  : {weather_desc}")
        print(f"Wind Speed : {weather.get('wind_speed_10m')} km/h")
        print(f"AQI (US)   : {aqi.get('us_aqi')} (PM2.5: {aqi.get('pm2_5')} µg/m³)\n")
    else:
        print("--- ⛅ Weather & Air Quality ---\nCould not retrieve data.\n")

    # Fetch Traffic
    traffic = get_traffic_info(API_KEYS["tomtom"], location["lat"], location["lon"])
    if traffic:
        print(f"--- 🚗 Traffic Report ---")
        print(f"{traffic['summary']}")
        # Print the detailed street-level issues if they exist
        for detail in traffic.get('details', []):
            print(f"  • {detail}")
        print("")
    else:
        print("--- 🚗 Traffic Report ---\nCould not retrieve data.\n")

    # Fetch News
    news = get_news_headlines(API_KEYS["newsapi"], location["city"], location["country_code"])
    if news:
        print("--- 📰 Top Headlines ---")
        for headline in news:
            print(f"{headline}\n")

    # Generate Health Report
    health_tips = generate_health_report(weather, aqi)
    print("--- 🩺 Health & Safety Briefing ---")
    for tip in health_tips:
        print(f"- {tip}")

    print("\n==================================================\n")


if __name__ == "__main__":
    main()