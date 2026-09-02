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
        
        # Add a quick health tip if available
        if health_tips and len(health_tips) > 0 and "optimal" not in health_tips[0].lower():
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
        headlines_to_read = news[:2]
        for idx, headline in enumerate(headlines_to_read):
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

def generate_radio_report_hindi(location, weather, aqi, weather_desc, traffic, news, health_tips):
    """
    Generates a Hinglish/Hindi radio-jockey style briefing.
    """
    city = location.get("city", "your area")
    
    # 1. Energetic Greeting (Hinglish RJ style)
    greetings = [
        f"Namaste {city}! Good morning aur swagat hai aapke daily briefing mein!",
        f"Kya haal hai {city}? Apni chai lijiye aur suniye aaj ka taza update!",
        f"Good morning {city}! Shuru karte hain aaj ki taaza khabaron ke sath!"
    ]
    
    report_parts = [random.choice(greetings)]
    
    # 2. Weather & Health
    if weather and aqi:
        temp = weather.get("temperature_2m", "unknown")
        feels_like = weather.get("apparent_temperature", "unknown")
        
        weather_phrases = [
            f"Mausam ki baat karein to, bahar {weather_desc.lower()} hai aur temperature {temp} degrees hai.",
            f"Aaj ka mausam {weather_desc.lower()} rahega, aur abhi temperature {temp} degrees chal raha hai."
        ]
        
        weather_sentence = random.choice(weather_phrases)
        
        if temp != "unknown" and feels_like != "unknown" and abs(temp - feels_like) >= 2:
            weather_sentence += f" Lekin dhyan rakhiye, feel actually {feels_like} degrees ka ho raha hai, toh apna khayal rakhein!"
            
        report_parts.append(weather_sentence)
        
        if health_tips and len(health_tips) > 0 and "optimal" not in health_tips[0].lower():
            clean_tip = health_tips[0].replace('🚨 ALERT:', 'Alert!').replace('🌡️', '').replace('❄️', '').replace('💧', '').replace('☔', '').replace('⛈️', '').replace('🌫️', '').replace('💨', '').replace('🟢', '').replace('🟡', '').replace('🟠', '').replace('🔴', '').strip()
            # Append English tip smoothly
            report_parts.append(f"Ek quick health update: {clean_tip}")
    else:
        report_parts.append("Mausam ka radar abhi kaam nahi kar raha, toh bahar dekh lijiye kaisa hai mausam!")

    # 3. Traffic
    if traffic:
        summary = traffic.get("summary", "")
        details = traffic.get("details", [])
        if "smoothly" in summary.lower():
            report_parts.append("Traffic ki baat karein toh roads bilkul smooth hain. Aaram se drive kijiye aaj!")
        else:
            report_parts.append("Roads par aaj thoda traffic jam mil sakta hai.")
            if details:
                incidents_to_read = details[:2]
                cleaned_incidents = [incident.replace("💥", "").replace("🚗", "").replace("🚧", "").replace("⛔", "").replace("⚠️", "").strip() for incident in incidents_to_read]
                report_parts.append(f"Specifically yahan dhyan de: {', aur '.join(cleaned_incidents)}.")
                if len(details) > 2:
                    report_parts.append("Kuch aur chote incidents bhi hain, toh drive safe!")
    else:
         report_parts.append("Traffic cameras se update nahi mil raha hai, par seatbelt lagaiye aur safe rahiye.")

    # 4. News
    if news and not news[0].startswith("NewsAPI key not set") and not news[0].startswith("No top headlines"):
        report_parts.append("Ab aate hain aaj ki taaza khabaron par.")
        headlines_to_read = news[:2]
        for idx, headline in enumerate(headlines_to_read):
            clean_headline = headline.replace("📰", "").split("\n")[0].strip()
            if idx == 0:
                report_parts.append(f"Pehli khabar: {clean_headline}.")
            else:
                report_parts.append(f"Aur doosri badi khabar: {clean_headline}.")
    else:
         report_parts.append("News desk par aaj shanti hai!")
         
    # 5. Energetic Sign-off
    sign_offs = [
        "Toh ye tha aaj ka update! Apna din enjoy kijiye, bye bye!",
        "Yehi hai aaj ka pura hisaab-kitaab! Khush rahiye, aur milte hain kal!",
        "Drive safe, apna khayal rakhiye, aur have a fantastic day!"
    ]
    report_parts.append(random.choice(sign_offs))
    
    return " ".join(report_parts)
