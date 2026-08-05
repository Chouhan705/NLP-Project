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