import random

def generate_radio_report(location, weather, aqi, weather_desc, traffic, news, health_tips):
    """
    Generates an energetic, upbeat radio-jockey style briefing.
    Includes failsafes for missing data.
    """
    city = location.get("city", "your area")
    
    # 1. Energetic Greeting
    greetings = [
        f"Hey there, {city}! Good morning and welcome to your daily run-down!",
        f"What's up, {city}? Grab your coffee because here is everything you need to know today!",
        f"Good morning {city}! Let's get you tuned in and ready to tackle the day!"
    ]
    
    report_parts = [random.choice(greetings)]
    
    # 2. Weather & Health
    if weather and aqi:
        temp = weather.get("temperature_2m", "unknown")
        feels_like = weather.get("apparent_temperature", "unknown")
        
        weather_phrases = [
            f"Looking at the skies, we've got {weather_desc.lower()} conditions out there with temperatures sitting around {temp} degrees.",
            f"Step outside and you'll find {weather_desc.lower()} weather, currently at {temp} degrees Celsius."
        ]
        
        weather_sentence = random.choice(weather_phrases)
        
        if temp != "unknown" and feels_like != "unknown" and abs(temp - feels_like) >= 2:
            weather_sentence += f" Just a heads up, though, it actually feels more like {feels_like} degrees, so dress accordingly!"
            
        report_parts.append(weather_sentence)
        
        # Add a quick health tip if available (filter out the default "all good" one for a better radio flow)
        if health_tips and len(health_tips) > 0 and "optimal" not in health_tips[0].lower():
            # Pick the most important health tip (first one), strip emojis
            clean_tip = health_tips[0].replace('🚨 ALERT:', 'Alert!').replace('🌡️', '').replace('❄️', '').replace('💧', '').replace('☔', '').replace('⛈️', '').replace('🌫️', '').replace('💨', '').replace('🟢', '').replace('🟡', '').replace('🟠', '').replace('🔴', '').strip()
            report_parts.append(f"Quick health check: {clean_tip}")
    else:
        report_parts.append("Our weather radar seems to be taking a coffee break right now, so maybe just peek out the window for the weather!")

    # 3. Traffic
    if traffic:
        summary = traffic.get("summary", "")
        details = traffic.get("details", [])
        if "smoothly" in summary.lower():
            report_parts.append("On the roads, things are flowing smoothly right now. Cruise control is your friend today!")
        else:
            report_parts.append("Looking at the traffic, we have a few slow-downs to watch out for.")
            if details:
                # Read out up to 2 incidents so it doesn't get boring
                incidents_to_read = details[:2]
                cleaned_incidents = [incident.replace("💥", "").replace("🚗", "").replace("🚧", "").replace("⛔", "").replace("⚠️", "").strip() for incident in incidents_to_read]
                report_parts.append(f"Specifically, watch out for: {', and '.join(cleaned_incidents)}.")
                if len(details) > 2:
                    report_parts.append("There are a few other minor incidents out there, so keep your eyes peeled and drive safe.")
    else:
         report_parts.append("We don't have eyes on the traffic cameras at the moment, so definitely buckle up and stay alert on the roads.")

    # 4. News
    if news and not news[0].startswith("NewsAPI key not set") and not news[0].startswith("No top headlines"):
        report_parts.append("Moving on to what's making headlines today.")
        # Just grab the top 2 headlines to keep it punchy
        headlines_to_read = news[:2]
        for idx, headline in enumerate(headlines_to_read):
            # Clean emojis and newlines for speech
            clean_headline = headline.replace("📰", "").split("\n")[0].strip()
            if idx == 0:
                report_parts.append(f"First up: {clean_headline}.")
            else:
                report_parts.append(f"Also in the news: {clean_headline}.")
    else:
         report_parts.append("The news desk is pretty quiet right now, which might just be a good thing!")
         
    # 5. Energetic Sign-off
    sign_offs = [
        "That's all for your morning briefing! Have an absolutely fantastic day out there!",
        "Alright, you're all caught up! Get out there and crush it today!",
        "And that's a wrap for your updates! Stay safe, stay awesome, and have a great one!"
    ]
    report_parts.append(random.choice(sign_offs))
    
    return " ".join(report_parts)
