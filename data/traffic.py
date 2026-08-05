import requests

from config import TRAFFIC_BBOX_PADDING, TRAFFIC_DETAILS_LIMIT


def get_traffic_info(api_key, lat, lon):
    """Fetches traffic incidents and extracts highly specific street locations, event descriptions, and delays."""
    if api_key == "YOUR_TOMTOM_API_KEY" or not api_key:
        return {"summary": "TomTom API key not set. Skipping traffic report.", "details": []}

    try:
        lat_f, lon_f = float(lat), float(lon)
        # Create a bounding box around the user's location
        bbox = (
            f"{lon_f - TRAFFIC_BBOX_PADDING},{lat_f - TRAFFIC_BBOX_PADDING},"
            f"{lon_f + TRAFFIC_BBOX_PADDING},{lat_f + TRAFFIC_BBOX_PADDING}"
        )

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

        # Limit to the top N most relevant issues to keep the report clean
        return {"summary": summary, "details": details[:TRAFFIC_DETAILS_LIMIT]}

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not fetch traffic data. Reason: {e}")
        return None