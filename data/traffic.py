import requests
from config import TRAFFIC_BBOX_PADDING, TRAFFIC_DETAILS_LIMIT


def get_street_name_from_coords(api_key, lat, lon):
    """Fallback: Resolves coordinates to a street or area name using TomTom Reverse Geocoding."""
    url = f"https://api.tomtom.com/search/2/reverseGeocode/{lat},{lon}.json?key={api_key}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            addresses = res.json().get("addresses", [])
            if addresses:
                address_info = addresses[0].get("address", {})
                street = address_info.get("streetName") or address_info.get("street")
                municipality = address_info.get("municipalitySubdivision") or address_info.get("municipality")
                
                if street and municipality:
                    return f"on {street} ({municipality})"
                elif street:
                    return f"on {street}"
                elif municipality:
                    return f"in {municipality}"
    except Exception:
        pass
    return None


def get_traffic_info(api_key, lat, lon):
    """Fetches traffic incidents and extracts street locations, event descriptions, and delays."""
    if api_key == "YOUR_TOMTOM_API_KEY" or not api_key:
        return {"summary": "TomTom API key not set. Skipping traffic report.", "details": []}

    try:
        lat_f, lon_f = float(lat), float(lon)
        bbox = (
            f"{lon_f - TRAFFIC_BBOX_PADDING},{lat_f - TRAFFIC_BBOX_PADDING},"
            f"{lon_f + TRAFFIC_BBOX_PADDING},{lat_f + TRAFFIC_BBOX_PADDING}"
        )

        url = f"https://api.tomtom.com/traffic/services/5/incidentDetails?key={api_key}&bbox={bbox}&language=en-GB"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        incidents = response.json().get('incidents', [])

        if not incidents:
            return {
                "summary": "Traffic appears to be flowing smoothly in your general vicinity.",
                "details": []
            }

        jams = sum(1 for inc in incidents if inc['properties'].get('iconCategory') == 6)
        accidents = sum(1 for inc in incidents if inc['properties'].get('iconCategory') == 1)
        roadworks = sum(1 for inc in incidents if inc['properties'].get('iconCategory') == 9)

        summary = f"Found {len(incidents)} incidents nearby: {jams} jam(s), {accidents} accident(s), {roadworks} roadwork(s)."

        details = []
        for inc in incidents:
            props = inc.get('properties', {})

            road_from = props.get('from', '')
            road_to = props.get('to', '')
            events = props.get('events', [])
            delay_seconds = props.get('delay', 0)
            icon_cat = props.get('iconCategory', 0)

            if icon_cat == 1:
                issue_type = "💥 Accident"
            elif icon_cat == 6:
                issue_type = "🚗 Traffic Jam"
            elif icon_cat == 9:
                issue_type = "🚧 Roadworks"
            elif icon_cat == 11:
                issue_type = "⛔ Road Closed"
            else:
                issue_type = "⚠️ Incident"

            event_desc = events[0].get('description', '') if events else ''

            # Construct location string
            if event_desc:
                location_str = event_desc
                if road_from and road_from.lower() not in location_str.lower():
                    location_str += f" (near {road_from})"
            elif road_from and road_to and road_from != road_to:
                location_str = f"on {road_from} (heading towards {road_to})"
            elif road_from:
                location_str = f"on {road_from}"
            else:
                # Dynamic Reverse Geocode Lookup when street names are missing
                geom = inc.get('geometry', {}).get('coordinates', [])
                resolved_location = None
                if geom and len(geom) > 0:
                    # TomTom geometry is [longitude, latitude] or nested list of coordinates
                    point = geom[0] if isinstance(geom[0], (int, float)) else geom[0][0] if isinstance(geom[0], list) else None
                    if isinstance(point, list) and len(point) >= 2:
                        resolved_location = get_street_name_from_coords(api_key, point[1], point[0])
                
                location_str = resolved_location if resolved_location else "on a local road"

            delay_str = f" - Delay: {delay_seconds // 60} mins" if delay_seconds >= 60 else ""
            detail_string = f"{issue_type} {location_str}{delay_str}"

            if detail_string not in details:
                details.append(detail_string)

        return {"summary": summary, "details": details[:TRAFFIC_DETAILS_LIMIT]}

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not fetch traffic data. Reason: {e}")
        return None