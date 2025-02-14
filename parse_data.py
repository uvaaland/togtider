# parse_data.py
import xml.etree.ElementTree as ET

def parse_departures(xml_response):
    # Define the namespace mapping (for SIRI namespace)
    namespaces = {"siri": "http://www.siri.org.uk/siri"}
    
    # Parse the XML response string
    root = ET.fromstring(xml_response)
    
    # List to hold departures from Jåttåvågen
    jattaavagen_departures = []
    
    # Find all EstimatedCall elements using XPath
    for call in root.findall(".//siri:EstimatedCall", namespaces):
        stop_ref_elem = call.find("siri:StopPointRef", namespaces)
        if stop_ref_elem is not None and stop_ref_elem.text == "NSR:Quay:609":
            aimed_dep = call.find("siri:AimedDepartureTime", namespaces)
            expected_dep = call.find("siri:ExpectedDepartureTime", namespaces)
            
            departure_info = {
                "StopPointRef": stop_ref_elem.text,
                "AimedDepartureTime": aimed_dep.text if aimed_dep is not None else None,
                "ExpectedDepartureTime": expected_dep.text if expected_dep is not None else None,
            }
            jattaavagen_departures.append(departure_info)
    
    return jattaavagen_departures

if __name__ == "__main__":
    # For testing purposes: parse a sample XML (you can replace this with an actual response)
    sample_xml = """PUT_YOUR_SAMPLE_XML_HERE"""
    departures = parse_departures(sample_xml)
    for dep in departures:
        print(dep)
