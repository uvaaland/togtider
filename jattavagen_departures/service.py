# jattavagen_departures/service.py
from .fetch_data import fetch_timetable
from .parse_data import parse_departures
from datetime import datetime, timedelta

def get_upcoming_departures():
    """
    Fetches the XML timetable, parses departures,
    filters out departures that have already passed,
    sorts them, and returns a dictionary with groups.
    """
    xml_response = fetch_timetable()
    departures = parse_departures(xml_response)
    
    # Get current time as offset-aware
    now = datetime.now().astimezone()
    
    # Filter and sort departures by adding the offset correction
    for group in departures.values():
        group[:] = [
            d for d in group 
            if (datetime.fromisoformat(d["AimedDepartureTime"]) + timedelta(hours=2)) >= now
        ]
        group.sort(key=lambda d: datetime.fromisoformat(d["AimedDepartureTime"]) + timedelta(hours=2))
    
    return departures

def format_departures(departures):
    """
    Format the departures into a JSON-friendly dict structure.
    """
    from datetime import datetime, timedelta

    def format_iso_timestamp(iso_str):
        dt = datetime.fromisoformat(iso_str) + timedelta(hours=2)
        return dt.strftime("%H:%M")
    
    formatted = {}
    for direction, deps in departures.items():
        formatted[direction] = []
        for dep in deps:
            aimed = format_iso_timestamp(dep['AimedDepartureTime'])
            actual = format_iso_timestamp(dep['ActualDepartureTime']) if dep['ActualDepartureTime'] else aimed
            status = "on schedule" if aimed == actual else "delayed"
            formatted[direction].append({
                "aimed": aimed,
                "actual": actual,
                "destination": dep['Destination'],
                "status": status
            })
    return formatted
