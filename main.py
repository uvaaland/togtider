# main.py
from fetch_data import fetch_timetable
from parse_data import parse_departures

def main():
    try:
        xml_response = fetch_timetable()
        departures = parse_departures(xml_response)
        
        if departures:
            print("Departures from Jåttåvågen:")
            for dep in departures:
                print(f"Aimed: {dep['AimedDepartureTime']}, Expected: {dep['ExpectedDepartureTime']}")
        else:
            print("No departures found for Jåttåvågen.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
