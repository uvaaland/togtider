# fetch_data.py
import requests
from config import API_ENDPOINT, SUBSCRIPTION_KEY, REQUESTOR_REF

def fetch_timetable():
    # Build the XML request body
    xml_request = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="http://www.siri.org.uk/siri" version="2.1"
      xmlns:xsd="http://www.w3.org/2001/XMLSchema"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <ServiceRequest>
    <RequestTimestamp>2025-02-14T10:00:00Z</RequestTimestamp>
    <RequestorRef>{REQUESTOR_REF}</RequestorRef>
    <EstimatedTimetableRequest version="1.1">
      <RequestTimestamp>2025-02-14T10:00:00Z</RequestTimestamp>
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
    
    response = requests.post(API_ENDPOINT, data=xml_request.encode('utf-8'), headers=headers)
    
    # Raise an exception if the request failed
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    # For testing purposes only
    print(fetch_timetable())
