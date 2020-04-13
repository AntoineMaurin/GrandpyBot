from unittest.mock import Mock, patch

import requests
import json

from gmaps_interaction import GmapsInteraction

class TestGmaps:

    def test_request(self):
        obj = GmapsInteraction()
        response = obj.request()
        assert response is not None

    def test_request_status_code(self):
        obj = GmapsInteraction()
        obj.request()
        assert obj.status_code < 400


    @patch('gmaps_interaction.requests.get')
    def test_request(self, mock_get):
        mock_get.return_value.ok = True

        obj = GmapsInteraction()
        response = obj.request()

        assert response is not None

# Test à adapter à G-Maps
    @patch('gmaps_interaction.requests.get')
    def test_json_response(self, mock_get):
        infos = [{
            "userId": 1,
            "id": 1,
            "title": "Do laudry",
            "completed": 'false'
            }]
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = infos

        obj = GmapsInteraction()
        response = obj.request()

        assert response.json() == infos



# Test transmission des données à la classe API Wiki
