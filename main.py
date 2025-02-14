# main.py
from fetch_data import fetch_timetable
from parse_data import parse_departures
from datetime import datetime

def format_iso_timestamp(iso_str):
    """
    Convert an ISO8601 timestamp string to a human-readable time format.
    Example: "2025-02-14T11:02:00+01:00" -> "11:02"
    """
    # Parse the ISO8601 string into a datetime object.
    # Note: fromisoformat is available in Python 3.7+.
    dt = datetime.fromisoformat(iso_str)
    # Format the datetime as HH:MM (24-hour clock)
    return dt.strftime("%H:%M")

def main():
    try:
        xml_response = fetch_timetable()
        departures = parse_departures(xml_response)
        
        if departures:
            print("Departures from Jåttåvågen:")
            for dep in departures:
                aimed = format_iso_timestamp(dep['AimedDepartureTime'])
                expected = format_iso_timestamp(dep['ExpectedDepartureTime'])
                
                # Check if the train is on schedule or delayed
                if aimed == expected:
                    status = "on schedule"
                else:
                    status = "delayed"
                
                print(f"Departure at {aimed} (expected: {expected}) - {status}")
        else:
            print("No departures found for Jåttåvågen.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
