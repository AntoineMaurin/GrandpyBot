from unittest.mock import Mock, patch

import requests
import re
import json

from wikimedia_interaction import WikimediaInteraction

class TestWikimedia:

    TEXT = "Cité Paradis"

    def test_search_arg(self):
        test = WikimediaInteraction(self.TEXT)
        assert test.search == self.TEXT

    def test_request_status_code(self):
        test = WikimediaInteraction(self.TEXT)
        test.request()
        assert test.status_code < 400

    @patch('wikimedia_interaction.requests.get')
    def test_request(self, mock_get):
        mock_get.return_value.ok = True
        test = WikimediaInteraction(self.TEXT)
        test_result = test.request()

        assert test_result is not None

    @patch('wikimedia_interaction.requests.get')
    def test_json_response(self, mock_get):
        infos = [{
            "query": {
                "pages": {
                    "5653202": {
                        "pageid": 5653202,
                        "ns": 0,
                        "title": "Cité Paradis",
                        "extract": "<p class=\"mw-empty-elt\">\n</p>\n<p>La <b>cité Paradis</b> est..."
                                }
                        }
                    }
        }]
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = infos

        test = WikimediaInteraction(self.TEXT)
        response = test.request()

        assert response.json() == infos

    # @patch('wikimedia_interaction.requests.get')
    # def test_conversion(self, mock_get):
    #     mock_get.return_value.ok = True
    #     test = WikimediaInteraction(self.TEXT)
    #     test_result = test.get_json_response()
    #     test_clean_text = test.cleanhtml(test_result)
    #
    #     assert re.search('<{1}>{1}', test_clean_text) == None
