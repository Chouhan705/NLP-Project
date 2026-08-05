# Paste your API keys here
API_KEYS = {
    "tomtom": "gqOPWMw3Bs3PodJzW0b7FkfZBjnfosWS",      # Your TomTom Key
    "newsapi": "94a5ec6d18494b89a2e940d88f0b3a34"        # Your NewsAPI Key
}

# WMO Weather interpretation codes -> human readable descriptions
WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm"
}

# Your location — set this once. IP-based geolocation was dropped since it's
# unreliable on mobile/broadband networks (your ISP's NAT gateway can be
# registered in a totally different city than where you actually are).
# Find your exact lat/lon at https://www.latlong.net if needed.
MY_LOCATION = {
    "city": "Mumbai",
    "country_code": "in",
    "lat": "19.0760",
    "lon": "72.8777"
}

# Bounding box padding (in degrees) used to build the traffic query area around a location
TRAFFIC_BBOX_PADDING = 0.05

# Max number of traffic incidents to include in the report
TRAFFIC_DETAILS_LIMIT = 6

# Max number of news articles to include in the report
NEWS_ARTICLES_LIMIT = 4

# Max length before a news description gets truncated
NEWS_DESCRIPTION_MAX_LEN = 180