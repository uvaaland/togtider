# main.py
from fetch_data import fetch_timetable
from parse_data import parse_departures
from datetime import datetime

def format_iso_timestamp(iso_str):
    """
    Convert an ISO8601 timestamp string to a human-readable time format.
    Example: "2025-02-14T11:02:00+01:00" -> "11:02"
    """
    dt = datetime.fromisoformat(iso_str)
    return dt.strftime("%H:%M")

def main():
    try:
        xml_response = fetch_timetable()
        departures = parse_departures(xml_response)
        
        # Print Southbound departures (assumed to have DirectionRef "EGS")
        if departures["southbound"]:
            print("Southbound Departures:")
            for dep in departures["southbound"]:
                aimed = format_iso_timestamp(dep['AimedDepartureTime'])
                # Use ActualDepartureTime if available; otherwise default to aimed
                actual = format_iso_timestamp(dep['ActualDepartureTime']) if dep['ActualDepartureTime'] else aimed
                status = "on schedule" if aimed == actual else "delayed"
                print(f"Departure at {aimed} (actual: {actual}) - {status}")
        else:
            print("No southbound departures found for Jåttåvågen.")
        
        print()  # Blank line between the groups
        
        # Print Northbound departures (all other DirectionRef values)
        if departures["northbound"]:
            print("Northbound Departures:")
            for dep in departures["northbound"]:
                aimed = format_iso_timestamp(dep['AimedDepartureTime'])
                actual = format_iso_timestamp(dep['ActualDepartureTime']) if dep['ActualDepartureTime'] else aimed
                status = "on schedule" if aimed == actual else "delayed"
                print(f"Departure at {aimed} (actual: {actual}) - {status}")
        else:
            print("No northbound departures found for Jåttåvågen.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
