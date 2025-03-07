# jattavagen_departures/parse_data.py
import logging
import xml.etree.ElementTree as ET
from datetime import datetime

# Set up logging
logger = logging.getLogger('togtider.parse')

def parse_departures(xml_response):
    """
    Parses the XML response and groups departures from Jåttåvågen by direction.
    
    Args:
        xml_response (str): XML response from the Bane NOR API
        
    Returns:
        dict: Dictionary with keys 'southbound' and 'northbound', each containing
              a list of departure dictionaries with information about each departure
              
    Raises:
        ValueError: If the XML parsing fails or response format is unexpected
    """
    if not xml_response or not isinstance(xml_response, str):
        logger.error("Invalid XML response provided")
        raise ValueError("Invalid XML response")
        
    try:
        # Define the namespace (the sample uses the default "siri" namespace)
        namespaces = {"siri": "http://www.siri.org.uk/siri"}
        
        logger.debug("Parsing XML response")
        root = ET.fromstring(xml_response)
        
        # We'll collect departures in a dictionary keyed by direction.
        departures = {"southbound": [], "northbound": []}
        
        # Accept both possible StopPointRef codes for Jåttåvågen
        valid_refs = {"NSR:Quay:609", "NSR:Quay:607"}
        
        # Ensure we found the root element correctly
        if root.tag != "{http://www.siri.org.uk/siri}Siri":
            logger.warning(f"Unexpected XML root tag: {root.tag}")
        
        # Count found journeys for logging
        journey_count = 0
        
        # Iterate over each EstimatedVehicleJourney
        for journey in root.findall(".//siri:EstimatedVehicleJourney", namespaces):
            journey_count += 1
            
            # Get the journey direction from DirectionRef.
            direction_elem = journey.find("siri:DirectionRef", namespaces)
            if direction_elem is None:
                logger.warning("Journey without DirectionRef found, skipping")
                continue
                
            direction_value = direction_elem.text.strip() if direction_elem.text else ""
            logger.debug(f"Found journey with direction: {direction_value}")
            
            # Here we determine if the journey is northbound or southbound
            # STV = Stavanger = northbound
            # EGS = Egersund = southbound
            if direction_value == "STV":
                dep_direction = "northbound"
            else:
                dep_direction = "southbound"
            
            # Extract the destination from the journey
            dest_elem = journey.find("siri:DestinationName", namespaces)
            destination = dest_elem.text.strip() if dest_elem is not None and dest_elem.text else "Unknown"
            
            # Process RecordedCalls for departures
            recorded_calls = journey.find("siri:RecordedCalls", namespaces)
            if recorded_calls is None:
                logger.warning(f"No RecordedCalls found for journey to {destination}")
                continue
            
            # Process each call (stop) in the journey
            call_count = 0
            for call in recorded_calls.findall("siri:RecordedCall", namespaces):
                call_count += 1
                stop_ref_elem = call.find("siri:StopPointRef", namespaces)
                
                # Skip stops that aren't at Jåttåvågen
                if stop_ref_elem is None or stop_ref_elem.text not in valid_refs:
                    continue
                
                # Extract departure times
                aimed_dep_elem = call.find("siri:AimedDepartureTime", namespaces)
                actual_dep_elem = call.find("siri:ActualDepartureTime", namespaces)
                
                # Create a departure info dictionary
                departure_info = {
                    "StopPointRef": stop_ref_elem.text,
                    "AimedDepartureTime": aimed_dep_elem.text if aimed_dep_elem is not None else None,
                    "ActualDepartureTime": actual_dep_elem.text if actual_dep_elem is not None else None,
                    "Direction": dep_direction,
                    "Destination": destination,
                }
                
                # Only add if we have a valid departure time
                if departure_info["AimedDepartureTime"]:
                    departures[dep_direction].append(departure_info)
                    logger.debug(f"Added {dep_direction} departure to {destination}")
                else:
                    logger.warning(f"Skipping departure without AimedDepartureTime")
            
            logger.debug(f"Processed {call_count} calls for journey")
            
        logger.info(f"Parsed {journey_count} journeys, found {len(departures['southbound']) + len(departures['northbound'])} departures")
        return departures
        
    except ET.ParseError as e:
        logger.error(f"XML parsing error: {str(e)}")
        raise ValueError(f"Failed to parse XML: {str(e)}")
    except Exception as e:
        logger.error(f"Error parsing departure data: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    # For testing purposes
    logging.basicConfig(level=logging.DEBUG)
    logger.info("This module can be tested by providing sample XML data")
    
    # Minimal test XML
    sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="http://www.siri.org.uk/siri">
    <ServiceDelivery>
        <EstimatedTimetableDelivery>
            <EstimatedJourneyVersionFrame>
                <EstimatedVehicleJourney>
                    <DirectionRef>EGS</DirectionRef>
                    <DestinationName>Egersund</DestinationName>
                    <RecordedCalls>
                        <RecordedCall>
                            <StopPointRef>NSR:Quay:609</StopPointRef>
                            <AimedDepartureTime>2025-03-07T10:15:00+01:00</AimedDepartureTime>
                            <ActualDepartureTime>2025-03-07T10:15:00+01:00</ActualDepartureTime>
                        </RecordedCall>
                    </RecordedCalls>
                </EstimatedVehicleJourney>
            </EstimatedJourneyVersionFrame>
        </EstimatedTimetableDelivery>
    </ServiceDelivery>
</Siri>
"""
    try:
        test_departures = parse_departures(sample_xml)
        for direction, deps in test_departures.items():
            print(f"{direction.capitalize()} departures:")
            for dep in deps:
                print(dep)
    except Exception as e:
        print(f"Test failed: {str(e)}")
