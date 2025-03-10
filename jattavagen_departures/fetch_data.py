# jattavagen_departures/fetch_data.py
import logging
import requests
from .config import API_ENDPOINT, SUBSCRIPTION_KEY, REQUESTOR_REF
from datetime import datetime

# Set up logging
logger = logging.getLogger('togtider.fetch')

def fetch_timetable():
    """
    Fetches timetable data from the Bane NOR API.
    
    Returns:
        str: XML response text from the API
        
    Raises:
        requests.RequestException: If the API request fails
        ValueError: If there's an issue with the API response
    """
    # Generate current time in ISO format
    current_time_iso = datetime.utcnow().isoformat() + "Z"
    logger.info(f"Fetching timetable at {current_time_iso}")
    
    # Build the XML request body dynamically
    xml_request = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="http://www.siri.org.uk/siri" version="2.1"
      xmlns:xsd="http://www.w3.org/2001/XMLSchema"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <ServiceRequest>
    <RequestTimestamp>{current_time_iso}</RequestTimestamp>
    <RequestorRef>{REQUESTOR_REF}</RequestorRef>
    <EstimatedTimetableRequest version="1.1">
      <RequestTimestamp>{current_time_iso}</RequestTimestamp>
      <PreviewInterval>PT120M</PreviewInterval>
      <OperatorRef>GOA</OperatorRef>
      <Lines>
        <LineDirection>
          <LineRef>GOA:Line:59</LineRef>
          <DirectionRef>EGS</DirectionRef>
        </LineDirection>
      </Lines>
      <StopPointRef>NSR:Quay:609</StopPointRef>
    </EstimatedTimetableRequest>
  </ServiceRequest>
</Siri>
"""

    headers = {
        "Content-Type": "application/xml",
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    }
    
    try:
        logger.debug(f"Sending request to {API_ENDPOINT}")
        response = requests.post(
            API_ENDPOINT, 
            data=xml_request.encode('utf-8'), 
            headers=headers,
            timeout=10  # Set a timeout to avoid hanging requests
        )
        response.raise_for_status()
        
        # Check if response is valid XML
        if not response.text.strip().startswith('<?xml'):
            logger.error(f"Invalid XML response: {response.text[:100]}...")
            raise ValueError("Invalid XML response received from API")
            
        logger.debug(f"Response received, status code: {response.status_code}")
        return response.text
    
    except requests.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during fetch: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    # Set up console logging for standalone testing
    logging.basicConfig(level=logging.DEBUG)
    print(fetch_timetable())
