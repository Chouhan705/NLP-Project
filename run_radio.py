import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import original data modules
from data.config import API_KEYS, WMO_CODES
from data.location import get_device_location
from data.weather import get_weather_and_aqi
from data.traffic import get_traffic_info
from data.news import get_news_headlines
from data.health import generate_health_report

# Import our new modules
from nlg.nlg_engine import generate_radio_report, generate_radio_report_hindi

def main():
    print("📻 Welcome to the Daily Briefing Studio!")
    
    print("\nPlease choose your language / भाषा चुनें:")
    print("1: English")
    print("2: Hindi (Hinglish)")
    lang_choice = input("Enter 1 or 2: ").strip()
    language = 'hi' if lang_choice == '2' else 'en'
    
    print("\nPlease choose your audio engine:")
    print("1: pyttsx3 (Offline, super fast)")
    print("2: edge-tts (Requires internet, highly energetic and natural)")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == '2':
        engine_choice = 'edge'
    else:
        engine_choice = 'pyttsx3'

    print(f"\n📻 Connecting to the Daily Briefing Studio ({language.upper()}, Engine: {engine_choice})...")
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
    print("\nGenerating natural language script...")
    if language == 'hi':
        script = generate_radio_report_hindi(
            location=location, weather=weather, aqi=aqi,
            weather_desc=weather_desc, traffic=traffic, news=news, health_tips=health_tips
        )
    else:
        script = generate_radio_report(
            location=location, weather=weather, aqi=aqi,
            weather_desc=weather_desc, traffic=traffic, news=news, health_tips=health_tips
        )
    
    print("\n" + "="*50)
    print("   📜 GENERATED SCRIPT FOR THE RJ")
    print("="*50)
    print(script)
    print("="*50 + "\n")
    
    # 3. Speak the script using the chosen engine
    if engine_choice == 'edge':
        from audio.edge_engine import speak_text_edge
        success = speak_text_edge(script, language=language)
    else:
        from audio.pyttsx3_engine import speak_text_pyttsx3
        success = speak_text_pyttsx3(script, language=language)
        
    if not success:
        print("\nFallback: Read the script above!\n")

if __name__ == "__main__":
    main()
