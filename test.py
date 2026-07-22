import requests
import geocoder
from datetime import datetime, timezone

# Location of your choice
def get_device_location():
    """
    Gets the device's location based on IP address.
    Falls back to a default location if unable to determine location.
    """
    try:
        print("INFO: Attempting to determine location automatically...")
        g = geocoder.ip('me')
        if g.ok and g.city:
            print(f"SUCCESS: Location found as {g.city}.")
            return {
                "city": g.city,
                "country_code": g.country.lower() if g.country else "in",
                "lat": str(g.lat),
                "lon": str(g.lng)
            }
        else:
            raise ValueError("Geocoder service returned a non-OK status.")
            
    except Exception as e:
        print(f"\n--- LOCATION DETECTION FAILED ---")
        print(f"REASON: {e}")
        print(f"Falling back to the default location (Mumbai).\n")
        return {
            "city": "Mumbai",
            "country_code": "in",
            "lat": "19.0760",
            "lon": "72.8777"
        }

# Get the location when the script starts
LOCATION = get_device_location()

# Paste your API keys here
API_KEYS = {
    "tomtom": "gqOPWMw3Bs3PodJzW0b7FkfZBjnfosWS",      # Your TomTom Key
    "newsapi": "94a5ec6d18494b89a2e940d88f0b3a34"        # Your NewsAPI Key
}

# --- 2. DATA FETCHING FUNCTIONS ---

WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm"
}

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
    

def get_traffic_info(api_key, lat, lon):
    """Fetches traffic incidents and extracts highly specific street locations, event descriptions, and delays."""
    if api_key == "YOUR_TOMTOM_API_KEY" or not api_key:
        return {"summary": "TomTom API key not set. Skipping traffic report.", "details": []}
        
    try:
        lat_f, lon_f = float(lat), float(lon)
        # Create a ~10km bounding box around the user's location
        bbox = f"{lon_f - 0.05},{lat_f - 0.05},{lon_f + 0.05},{lat_f + 0.05}"
        
        url = f"https://api.tomtom.com/traffic/services/5/incidentDetails?key={api_key}&bbox={bbox}&language=en-GB"
        response = requests.get(url)
        response.raise_for_status()
        
        incidents = response.json().get('incidents', [])
        
        if not incidents:
            return {
                "summary": "Traffic appears to be flowing smoothly in your general vicinity.", 
                "details": []
            }
        
        # Calculate summary counts
        jams = sum(1 for inc in incidents if inc['properties']['iconCategory'] == 6)
        accidents = sum(1 for inc in incidents if inc['properties']['iconCategory'] == 1)
        roadworks = sum(1 for inc in incidents if inc['properties']['iconCategory'] == 9)
        
        summary = f"Found {len(incidents)} incidents nearby: {jams} jam(s), {accidents} accident(s), {roadworks} roadwork(s)."
        
        # Extract specific street data
        details = []
        for inc in incidents:
            props = inc.get('properties', {})
            
            # Grab all possible location clues from TomTom
            road_from = props.get('from', '')
            road_to = props.get('to', '')
            events = props.get('events', [])
            delay_seconds = props.get('delay', 0)
            icon_cat = props.get('iconCategory', 0)
            
            # Map incident types
            if icon_cat == 1: issue_type = "💥 Accident"
            elif icon_cat == 6: issue_type = "🚗 Traffic Jam"
            elif icon_cat == 9: issue_type = "🚧 Roadworks"
            elif icon_cat == 11: issue_type = "⛔ Road Closed"
            else: issue_type = "⚠️ Incident"

            # 1. Best Scenario: TomTom provides an exact descriptive text (e.g. "Stationary traffic on Ghodbunder Rd")
            event_desc = events[0].get('description', '') if events else ''
            
            # Construct the smartest location string possible
            if event_desc:
                location_str = event_desc
                # Sometimes the description lacks the exact street, but 'from' has it. Let's combine them safely.
                if road_from and road_from.lower() not in location_str.lower():
                    location_str += f" (near {road_from})"
            # 2. Good Scenario: We have a Start and End street name
            elif road_from and road_to and road_from != road_to:
                location_str = f"on {road_from} (heading towards {road_to})"
            # 3. Okay Scenario: We just have one street name
            elif road_from:
                location_str = f"on {road_from}"
            # 4. Fallback: No street names available, use exact coordinates of the jam
            else:
                geom = inc.get('geometry', {}).get('coordinates', [])
                if geom and len(geom) > 0:
                    # TomTom returns [longitude, latitude]
                    location_str = f"at coordinates {geom[0][1]:.4f}, {geom[0][0]:.4f}"
                else:
                    location_str = "on a local road"

            # Format the delay time beautifully
            delay_str = f" - Delay: {delay_seconds // 60} mins" if delay_seconds >= 60 else ""
            
            # Combine everything into one string
            detail_string = f"{issue_type} {location_str}{delay_str}"
            
            # Prevent duplicates
            if detail_string not in details:
                details.append(detail_string)
                
        # Limit to the top 6 most relevant issues to keep the report clean
        return {"summary": summary, "details": details[:6]}

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not fetch traffic data. Reason: {e}")
        return None
    
def get_news_headlines(api_key, city, country_code):
    """Fetches top news headlines, including source and detailed descriptions."""
    if api_key == "YOUR_NEWSAPI_KEY":
        return ["NewsAPI key not set. Skipping news report."]

    def extract_article_details(articles_data):
        """Helper to format the headline with descriptions."""
        formatted_news = []
        for art in articles_data[:4]: # Grab up to top 4 stories
            title = art.get('title', 'No Title')
            desc = art.get('description', '')
            source = art.get('source', {}).get('name', 'Unknown Source')
            
            # Clean up NewsAPI titles (they often put "- Source" at the end of the title)
            if title and f" - {source}" in title:
                title = title.replace(f" - {source}", "")
                
            # Create a more detailed layout
            article_text = f"📰 {title} (Via {source})"
            if desc and desc != "null":
                # Truncate description slightly if it's overly massive
                desc_short = (desc[:180] + '...') if len(desc) > 180 else desc
                article_text += f"\n   ↳ {desc_short}"
                
            formatted_news.append(article_text)
        return formatted_news

    try:
        # 1st Attempt: Highly specific city news
        specific_url = f"https://newsapi.org/v2/everything?q={city}&sortBy=relevancy&pageSize=4&apiKey={api_key}"
        response = requests.get(specific_url)
        
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            if articles:
                return extract_article_details(articles)

        # 2nd Attempt: Fallback to broader country search
        print("INFO: Broadening news search to country level...")
        general_url = f"https://newsapi.org/v2/top-headlines?country={country_code}&pageSize=4&apiKey={api_key}"
        response = requests.get(general_url)
        response.raise_for_status()
        
        articles = response.json().get('articles', [])
        if articles:
            return extract_article_details(articles)
        else:
            return ["No top headlines found for your region at the moment."]

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not fetch news data. Reason: {e}")
        return None

# --- 3. HEALTH REPORT GENERATOR ---
# (Remains the same as the previous improved version)

def generate_health_report(weather, aqi):
    recommendations = []
    
    if aqi:
        aqi_value = aqi.get('us_aqi', 50)
        pm25 = aqi.get('pm2_5', 0)
        
        if aqi_value <= 50:
            recommendations.append("🟢 Air quality is Excellent! Great day for outdoor activities.")
        elif 50 < aqi_value <= 100:
            recommendations.append("🟡 Air quality is Moderate. Safe for most, but unusually sensitive people should limit heavy exertion.")
        elif 100 < aqi_value <= 150:
            recommendations.append("🟠 Air quality is Unhealthy for Sensitive Groups. Asthma/allergy sufferers should stay indoors.")
        elif 150 < aqi_value <= 200:
            recommendations.append("🔴 Air quality is Unhealthy. Everyone should reduce heavy outdoor exertion.")
        else:
            recommendations.append("🚨 ALERT: Air quality is Hazardous. Avoid outdoor activities. Wear an N95 mask if you must go outside.")
            
        if pm25 > 35:
            recommendations.append(f"   - Note: PM2.5 levels are elevated ({pm25} µg/m³). Keep your windows closed.")

    if weather:
        temp = weather.get('temperature_2m', 20)
        feels_like = weather.get('apparent_temperature', temp)
        weather_code = weather.get('weather_code', 0)
        wind = weather.get('wind_speed_10m', 0)
        
        if feels_like >= 35:
            recommendations.append(f"🌡️ Extreme Heat: It feels like {feels_like}°C. Stay severely hydrated and avoid afternoon sun.")
        elif feels_like < 10:
            recommendations.append(f"❄️ Cold Weather: It feels like {feels_like}°C. Bundle up in warm layers before heading out.")
        elif feels_like > temp + 3:
            recommendations.append(f"💧 High Humidity: Temperature is {temp}°C but feels like {feels_like}°C due to humidity.")
        
        if weather_code in [61, 63, 65, 80, 81, 82]:
             recommendations.append("☔ Rain is currently expected. Roads may be slick; carry an umbrella.")
        elif weather_code in [95]:
             recommendations.append("⛈️ Thunderstorms active! Unplug sensitive electronics and stay indoors.")
        elif weather_code in [45, 48]:
             recommendations.append("🌫️ Dense Fog reported. Reduce driving speeds and use low-beam headlights.")
             
        if wind > 40:
             recommendations.append(f"💨 High Winds Alert: Speeds reaching {wind} km/h. Secure loose outdoor objects.")

    if not recommendations:
        return ["✅ Conditions are optimal. Have a great day!"]
        
    return recommendations

# --- 4. MAIN EXECUTION ---

def main():
    print(f"\n{'='*50}")
    print(f"   DAILY BRIEFING FOR {LOCATION['city'].upper()} ")
    print(f"{'='*50}\n")

    # Fetch Weather and AQI
    weather, aqi = get_weather_and_aqi(LOCATION["lat"], LOCATION["lon"])
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
    traffic = get_traffic_info(API_KEYS["tomtom"], LOCATION["lat"], LOCATION["lon"])
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
    news = get_news_headlines(API_KEYS["newsapi"], LOCATION["city"], LOCATION["country_code"])
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