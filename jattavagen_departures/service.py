# jattavagen_departures/service.py
import logging
from .fetch_data import fetch_timetable
from .parse_data import parse_departures
from datetime import datetime, timedelta

# Set up logging
logger = logging.getLogger('togtider.service')

def get_upcoming_departures():
    """
    Fetches the XML timetable, parses departures,
    filters out departures that have already passed,
    sorts them, and returns a dictionary with groups.
    """
    logger.info("Fetching timetable data")
    try:
        xml_response = fetch_timetable()
        logger.debug("XML data fetched successfully, parsing departures")
        departures = parse_departures(xml_response)
        
        # Get current time as offset-aware
        now = datetime.now().astimezone()
        logger.debug(f"Current time: {now.isoformat()}")
        
        # Filter and sort departures by adding the offset correction
        for direction, group in departures.items():
            logger.debug(f"Processing {len(group)} {direction} departures")
            group[:] = [
                d for d in group 
                if (datetime.fromisoformat(d["AimedDepartureTime"]) + timedelta(hours=2)) >= now
            ]
            group.sort(key=lambda d: datetime.fromisoformat(d["AimedDepartureTime"]) + timedelta(hours=2))
            logger.debug(f"After filtering: {len(group)} {direction} departures remaining")
        
        return departures
    except Exception as e:
        logger.error(f"Error getting departures: {str(e)}", exc_info=True)
        raise

def format_departures(departures):
    """
    Format the departures into a JSON-friendly dict structure.
    """
    from datetime import datetime, timedelta
    
    logger.info("Formatting departure data")
    
    def format_iso_timestamp(iso_str):
        dt = datetime.fromisoformat(iso_str) + timedelta(hours=2)
        return dt.strftime("%H:%M")
    
    formatted = {
        "timestamp": datetime.now().isoformat()
    }
    
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
    
    logger.info(f"Formatted {sum(len(deps) for deps in departures.values())} departures")
    return formatted
