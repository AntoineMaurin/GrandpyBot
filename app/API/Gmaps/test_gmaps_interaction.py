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
        assert response == ('Lieu introuvable sur Google Maps')

    # @patch('gmaps_interaction.GmapsInteraction.get_content')
    # def test_get_content(self, mock_get_content):
    #     infos = ('6 Cité Paradis, 75010 Paris', 33.501, 28.904)
    #     mock_get_content.return_value = infos
    #
    #     test = GmapsInteraction(self.TEXT)
    #     response = test.get_content()
    #     assert response == infos

# Test transmission des données à la classe API Wiki
