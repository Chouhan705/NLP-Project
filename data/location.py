import geocoder

from config import DEFAULT_LOCATION


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
        print(f"Falling back to the default location ({DEFAULT_LOCATION['city']}).\n")
        return DEFAULT_LOCATION