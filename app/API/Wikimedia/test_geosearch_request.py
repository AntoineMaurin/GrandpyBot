from app.API.Wikimedia.geosearch_request import GeoSearchRequest
from unittest.mock import Mock, patch

import pytest
import json

class TestGeoSearchRequest:

    POS = (48.8748465, 2.3504873)
    DATA = {
            "batchcomplete": "",
            "query": {
                "geosearch": [
                        {
                        "pageid": 5653202,
                        "ns": 0,
                        "title": "Cité Paradis",
                        "lat": 48.87409,
                        "lon": 2.35064,
                        "dist": 84.9,
                        "primary": ""
                        },
                        {
                        "pageid": 6035646,
                        "ns": 0,
                        "title": "Hôtel Botterel de Quintin",
                        "lat": 48.8742,
                        "lon": 2.34989,
                        "dist": 84.1,
                        "primary": ""
                        }
                    ]
                }
            }

    @patch('app.API.Wikimedia.geosearch_request.requests.get')
    def setup_function(self, mock_text):
        mock_text.return_value.text = self.DATA

    def test_dict_tranform(self):
        r = GeoSearchRequest.request(self.POS)
        assert isinstance(r, dict)

    @patch('app.API.Wikimedia.geosearch_request.requests.get')
    def test_return_value_when_error(self, mock_bad_status_code):
        mock_bad_status_code.return_value.status_code = 404
        r = GeoSearchRequest.request(self.POS)
        assert isinstance(r, str)

    @patch('app.API.Wikimedia.geosearch_request.requests.get')
    def test_bad_status_code(self, mock_bad_status_code):
        mock_bad_status_code.return_value.status_code = 404
        response = GeoSearchRequest.request(self.POS)
        assert response == "Problème pour contacter l'API Wikimedia"
