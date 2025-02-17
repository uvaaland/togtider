# tests/test_service.py
import unittest
from datetime import datetime, timedelta
from jattavagen_departures.service import get_upcoming_departures, format_departures

class TestDepartureService(unittest.TestCase):
    def test_format_departures(self):
        # Create a dummy departures dict similar to what get_upcoming_departures returns.
        dummy_departures = {
            "southbound": [{
                "AimedDepartureTime": (datetime.now().astimezone() + timedelta(minutes=10)).isoformat(),
                "ActualDepartureTime": (datetime.now().astimezone() + timedelta(minutes=10)).isoformat(),
                "Destination": "Egersund",
                "Direction": "southbound"
            }],
            "northbound": [{
                "AimedDepartureTime": (datetime.now().astimezone() + timedelta(minutes=20)).isoformat(),
                "ActualDepartureTime": (datetime.now().astimezone() + timedelta(minutes=22)).isoformat(),
                "Destination": "Stavanger",
                "Direction": "northbound"
            }]
        }
        
        formatted = format_departures(dummy_departures)
        # Assert that the formatted output contains keys for southbound and northbound
        self.assertIn("southbound", formatted)
        self.assertIn("northbound", formatted)
        # Assert that the output is a list and contains expected keys
        self.assertIsInstance(formatted["southbound"], list)
        if formatted["southbound"]:
            self.assertIn("aimed", formatted["southbound"][0])
            self.assertIn("destination", formatted["southbound"][0])

if __name__ == '__main__':
    unittest.main()
