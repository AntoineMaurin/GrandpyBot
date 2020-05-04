from gmaps_request import GmapsRequest
from unittest.mock import patch


class TestGmapsRequest:

    TEXT = "OpenClassrooms"
    DATA = {"results": [{
                    "formatted_address": "7 Cité Paradis, 75010 Paris, France",
                    "geometry": {
                      "location": {
                          "lat": 48.8748465,
                          "lng": 2.3504873
                                        }
                                }
                    }]}

    @patch('app.API.Gmaps.gmaps_request.requests.get')
    def setup_function(self, mock_text):
        mock_text.return_value.text = str(self.DATA)

    @patch('app.API.Gmaps.gmaps_request.requests.get')
    def test_return_value_when_error(self, mock_bad_status_code):
        mock_bad_status_code.return_value.status_code = 404
        r = GmapsRequest.request(self.TEXT)
        assert isinstance(r, str)

    @patch('app.API.Gmaps.gmaps_request.requests.get')
    def test_bad_status_code(self, mock_bad_status_code):
        mock_bad_status_code.return_value.status_code = 404
        response = GmapsRequest.request(self.TEXT)
        assert response == "Problème pour contacter l'API Google Places"
