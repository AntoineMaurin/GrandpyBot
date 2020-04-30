from unittest.mock import Mock, patch

import requests
import json

from gmaps_interaction import GmapsInteraction

class TestGmapsInteraction:

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

    def test_search_arg(self):
        obj = GmapsInteraction(self.TEXT)
        assert obj.search == self.TEXT

    @patch('app.API.Gmaps.gmaps_request.GmapsRequest.request')
    def test_type_final_content(self, mock_data):
        mock_data.return_value = self.DATA
        obj = GmapsInteraction(self.TEXT)
        response = obj.get_content()
        assert isinstance(response, dict)

    @patch('app.API.Gmaps.gmaps_request.GmapsRequest.request')
    def test_final_content(self, mock_data):
        mock_data.return_value = self.DATA
        obj = GmapsInteraction(self.TEXT)
        response = obj.get_content()
        expected_result = {'address': '7 Cité Paradis, 75010 Paris, France',
                           'lat': 48.8748465,
                           'lng': 2.3504873
                          }
        assert response == expected_result

    @patch('app.API.Gmaps.gmaps_request.GmapsRequest.request')
    def test_index_error(self, mock_bad_dict):
        bad_dict = {
                       "html_attributions" : [],
                       "results" : [],
                       "status" : "ZERO_RESULTS"
                    }
        mock_bad_dict.return_value = bad_dict
        obj = GmapsInteraction('Poudlard')
        response = obj.get_content()
        supposed_response = {}
        supposed_response['error_msg'] = ("Je n'ai pas bien compris"
                                          " ta question, veux-tu reformuler"
                                          " s'il te plaît ?")
        assert response == supposed_response
