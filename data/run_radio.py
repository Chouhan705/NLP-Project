from config import API_KEYS, WMO_CODES
from location import get_device_location
from weather import get_weather_and_aqi
from traffic import get_traffic_info
from news import get_news_headlines
from health import generate_health_report

from nlg import generate_radio_report
from audio import speak_text

def main():
    print("📻 Connecting to the Daily Briefing Studio...")
    print("Gathering data...\n")
    
    # 1. Fetch Data
    location = get_device_location()
    weather, aqi = get_weather_and_aqi(location["lat"], location["lon"])
    
    weather_desc = "Unknown"
    if weather:
        weather_desc = WMO_CODES.get(weather.get('weather_code', -1), "Unknown Condition")
        
    traffic = get_traffic_info(API_KEYS["tomtom"], location["lat"], location["lon"])
    news = get_news_headlines(API_KEYS["newsapi"], location["city"], location["country_code"])
    
    health_tips = []
    if weather and aqi:
        health_tips = generate_health_report(weather, aqi)
        
    # 2. Generate the Radio-style NLG script
    print("Generating natural language script...")
    script = generate_radio_report(
        location=location,
        weather=weather,
        aqi=aqi,
        weather_desc=weather_desc,
        traffic=traffic,
        news=news,
        health_tips=health_tips
    )
    
    print("\n" + "="*50)
    print("   📜 GENERATED SCRIPT FOR THE RJ")
    print("="*50)
    print(script)
    print("="*50 + "\n")
    
    # 3. Speak the script
    speak_text(script)

if __name__ == "__main__":
    main()
