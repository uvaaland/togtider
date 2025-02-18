# jattavagen_departures/parse_data.py
import xml.etree.ElementTree as ET

def parse_departures(xml_response):
    """
    Parses the XML response and groups departures from Jåttåvågen by direction.
    A departure is only added if its StopPointRef is one of the two codes for Jåttåvågen.
    The journey’s DirectionRef is used to determine if the departure is southbound or northbound.
    Additionally, the destination is extracted from the journey.
    """
    # Define the namespace (the sample uses the default "siri" namespace)
    namespaces = {"siri": "http://www.siri.org.uk/siri"}
    
    root = ET.fromstring(xml_response)
    # We'll collect departures in a dictionary keyed by direction.
    departures = {"southbound": [], "northbound": []}
    
    # Accept both possible StopPointRef codes for Jåttåvågen
    valid_refs = {"NSR:Quay:609", "NSR:Quay:607"}
    
    # Iterate over each EstimatedVehicleJourney
    for journey in root.findall(".//siri:EstimatedVehicleJourney", namespaces):
        # Get the journey direction from DirectionRef.
        direction_elem = journey.find("siri:DirectionRef", namespaces)
        if direction_elem is None:
            continue
        direction_value = direction_elem.text.strip() if direction_elem.text else ""
        # Here we assume that "EGS" indicates a southbound journey,
        # while any other value is taken to be northbound.
        if direction_value == "STV":
            dep_direction = "northbound"
        else:
            dep_direction = "southbound"
        
        # Also extract the destination from the journey
        dest_elem = journey.find("siri:DestinationName", namespaces)
        destination = dest_elem.text.strip() if dest_elem is not None and dest_elem.text else "Unknown"
        
        # Process RecordedCalls for departures
        recorded_calls = journey.find("siri:RecordedCalls", namespaces)
        if recorded_calls is None:
            continue
        
        for call in recorded_calls.findall("siri:RecordedCall", namespaces):
            stop_ref_elem = call.find("siri:StopPointRef", namespaces)
            if stop_ref_elem is None or stop_ref_elem.text not in valid_refs:
                continue
            
            aimed_dep_elem = call.find("siri:AimedDepartureTime", namespaces)
            actual_dep_elem = call.find("siri:ActualDepartureTime", namespaces)
            
            departure_info = {
                "StopPointRef": stop_ref_elem.text,
                "AimedDepartureTime": aimed_dep_elem.text if aimed_dep_elem is not None else None,
                "ActualDepartureTime": actual_dep_elem.text if actual_dep_elem is not None else None,
                "Direction": dep_direction,
                "Destination": destination,
            }
            departures[dep_direction].append(departure_info)
            
    return departures

if __name__ == "__main__":
    # For testing purposes: parse a sample XML (replace with your actual response)
    sample_xml = """PUT_YOUR_SAMPLE_XML_HERE"""
    departures = parse_departures(sample_xml)
    for direction, deps in departures.items():
        print(f"{direction.capitalize()} departures:")
        for dep in deps:
            print(dep)
