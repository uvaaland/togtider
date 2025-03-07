# tests/test_service.py
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from jattavagen_departures.service import get_upcoming_departures, format_departures

class TestDepartureService(unittest.TestCase):
    def test_format_departures(self):
        """Test that departures are properly formatted"""
        # Create a dummy departures dict similar to what get_upcoming_departures returns.
        current_time = datetime.now().astimezone()
        dummy_departures = {
            "southbound": [{
                "AimedDepartureTime": (current_time + timedelta(minutes=10)).isoformat(),
                "ActualDepartureTime": (current_time + timedelta(minutes=10)).isoformat(),
                "Destination": "Egersund",
                "Direction": "southbound"
            }],
            "northbound": [{
                "AimedDepartureTime": (current_time + timedelta(minutes=20)).isoformat(),
                "ActualDepartureTime": (current_time + timedelta(minutes=22)).isoformat(),
                "Destination": "Stavanger",
                "Direction": "northbound"
            }]
        }
        
        formatted = format_departures(dummy_departures)
        
        # Assert that the formatted output contains keys for southbound and northbound
        self.assertIn("southbound", formatted)
        self.assertIn("northbound", formatted)
        self.assertIn("timestamp", formatted)
        
        # Assert that the output is a list and contains expected keys
        self.assertIsInstance(formatted["southbound"], list)
        self.assertIsInstance(formatted["northbound"], list)
        
        # Check southbound departure
        if formatted["southbound"]:
            self.assertIn("aimed", formatted["southbound"][0])
            self.assertIn("actual", formatted["southbound"][0])
            self.assertIn("destination", formatted["southbound"][0])
            self.assertIn("status", formatted["southbound"][0])
            self.assertEqual(formatted["southbound"][0]["destination"], "Egersund")
            self.assertEqual(formatted["southbound"][0]["status"], "on schedule")
        
        # Check northbound departure
        if formatted["northbound"]:
            self.assertIn("aimed", formatted["northbound"][0])
            self.assertIn("actual", formatted["northbound"][0])
            self.assertIn("destination", formatted["northbound"][0])
            self.assertIn("status", formatted["northbound"][0])
            self.assertEqual(formatted["northbound"][0]["destination"], "Stavanger")
            self.assertEqual(formatted["northbound"][0]["status"], "delayed")
    
    @patch('jattavagen_departures.service.fetch_timetable')
    @patch('jattavagen_departures.service.parse_departures')
    def test_get_upcoming_departures(self, mock_parse, mock_fetch):
        """Test that departures are fetched, filtered and sorted"""
        # Mock the API response
        mock_fetch.return_value = "<xml>dummy xml</xml>"
        
        # Set up the mock parse_departures to return test data
        current_time = datetime.now().astimezone()
        past_time = (current_time - timedelta(minutes=10)).isoformat()
        future_time1 = (current_time + timedelta(minutes=10)).isoformat()
        future_time2 = (current_time + timedelta(minutes=20)).isoformat()
        
        mock_parse.return_value = {
            "southbound": [
                {
                    "AimedDepartureTime": past_time,
                    "ActualDepartureTime": past_time,
                    "Destination": "Egersund",
                    "Direction": "southbound"
                },
                {
                    "AimedDepartureTime": future_time2,
                    "ActualDepartureTime": future_time2,
                    "Destination": "Egersund",
                    "Direction": "southbound"
                },
                {
                    "AimedDepartureTime": future_time1,
                    "ActualDepartureTime": future_time1,
                    "Destination": "Nærbø",
                    "Direction": "southbound"
                }
            ],
            "northbound": []
        }
        
        # Call the function
        result = get_upcoming_departures()
        
        # Verify that API was called
        mock_fetch.assert_called_once()
        mock_parse.assert_called_once_with("<xml>dummy xml</xml>")
        
        # Verify filtering of past departures
        self.assertEqual(len(result["southbound"]), 2)
        
        # Verify sorting
        self.assertEqual(result["southbound"][0]["Destination"], "Nærbø")
        self.assertEqual(result["southbound"][1]["Destination"], "Egersund")

if __name__ == '__main__':
    unittest.main()
