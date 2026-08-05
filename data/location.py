from config import MY_LOCATION


def get_device_location():
    """
    Returns your configured location.

    IP-based geolocation was removed — it's unreliable on mobile/broadband
    networks where your ISP's IP block can be registered far from your
    actual city. Update MY_LOCATION in config.py if you move.
    """
    return MY_LOCATION