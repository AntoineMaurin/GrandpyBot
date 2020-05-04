from gmaps_interaction import GmapsInteraction
from unittest.mock import patch


class TestGmapsInteraction:

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
                       "html_attributions": [],
                       "results": [],
                       "status": "ZERO_RESULTS"
                    }
        mock_bad_dict.return_value = bad_dict
        obj = GmapsInteraction('Poudlard')
        response = obj.get_content()
        supposed_response = {}
        supposed_response['error_msg'] = ("Qu'est ce que tu dis ? " +
                                          obj.search + " ? Je ne connais pas "
                                          "ce lieu, ou peut-être ai-je mal "
                                          "compris.. veux-tu reformuler s'il "
                                          "te plaît ?")

        assert response['error_msg'] == supposed_response['error_msg']
