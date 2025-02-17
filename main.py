# main.py
from fetch_data import fetch_timetable
from parse_data import parse_departures
from datetime import datetime, timedelta

def format_iso_timestamp(iso_str):
    """
    Convert an ISO8601 timestamp string to a human-readable time format,
    adjusted by adding 2 hours. For example:
      "2025-02-17T11:02:00+01:00" -> "13:02"
    """
    dt = datetime.fromisoformat(iso_str)
    # Add a two-hour offset to correct the reported time
    dt_corrected = dt + timedelta(hours=2)
    return dt_corrected.strftime("%H:%M")

def main():
    try:
        xml_response = fetch_timetable()
        departures = parse_departures(xml_response)
        
        # Get the current local time as an offset-aware datetime
        now = datetime.now().astimezone()
        
        # Filter out departures that have already happened.
        # We compare the corrected aimed departure time with the current time.
        for group in departures.values():
            group[:] = [
                d for d in group 
                if (datetime.fromisoformat(d["AimedDepartureTime"]) + timedelta(hours=2)) >= now
            ]
        
        # Sort departures in each group by their corrected AimedDepartureTime
        for group in departures.values():
            group.sort(key=lambda d: datetime.fromisoformat(d["AimedDepartureTime"]) + timedelta(hours=2))
        
        # Print Southbound departures (assumed to have DirectionRef "EGS")
        if departures["southbound"]:
            print("Southbound Departures:")
            for dep in departures["southbound"]:
                aimed = format_iso_timestamp(dep['AimedDepartureTime'])
                actual = format_iso_timestamp(dep['ActualDepartureTime']) if dep['ActualDepartureTime'] else aimed
                status = "on schedule" if aimed == actual else "delayed"
                print(f"Departure at {aimed} (actual: {actual}) to {dep['Destination']} - {status}")
        else:
            print("No upcoming southbound departures found for Jåttåvågen.")
        
        print()  # Blank line between the groups
        
        # Print Northbound departures (all other DirectionRef values)
        if departures["northbound"]:
            print("Northbound Departures:")
            for dep in departures["northbound"]:
                aimed = format_iso_timestamp(dep['AimedDepartureTime'])
                actual = format_iso_timestamp(dep['ActualDepartureTime']) if dep['ActualDepartureTime'] else aimed
                status = "on schedule" if aimed == actual else "delayed"
                print(f"Departure at {aimed} (actual: {actual}) to {dep['Destination']} - {status}")
        else:
            print("No upcoming northbound departures found for Jåttåvågen.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
