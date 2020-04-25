from gmaps_request import GmapsRequest
from unittest.mock import Mock, patch

import pytest, json

from gmaps_request import GmapsRequest

class TestGmapsRequest:

    TEXT = "OpenClassrooms"
    DATA = {"results" : [{
                    "formatted_address" : "7 Cité Paradis, 75010 Paris, France",
                    "geometry" : {
                          "location" : {
                          "lat" : 48.8748465,
                          "lng" : 2.3504873
                                        }
                                }
                    }]}

    @patch('app.API.Gmaps.gmaps_request.requests.get')
    def setup_function(self, mock_text):
        mock_text.return_value.text = str(self.DATA)

    def test_dict_tranform(self):
        r = GmapsRequest.request(self.TEXT)
        assert isinstance(r, dict)

    def test_dict_tranform_fails(self):
        r = GmapsRequest.request(self.TEXT)
        with pytest.raises(AssertionError):
            assert not isinstance(r, dict)

    @patch('gmaps_request.requests.get')
    def test_bad_status_code(self, mock_bad_status_code):
        mock_bad_status_code.return_value.status_code = 404
        response = GmapsRequest.request(self.TEXT)
        assert response == "Problème pour contacter l'API Google Places"
