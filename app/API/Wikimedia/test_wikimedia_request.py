from wikimedia_request import WikimediaRequest
from unittest.mock import Mock, patch

import pytest, json

class TestWikimediaRequest:

    URL = "https://fr.wikipedia.org/w/api.php?action=query&format=json&"
    "prop=extracts&titles=Cité%20Paradis&redirects=1&exsentences=4"

    def test_url_attribute(self):
        response = WikimediaRequest.request(self.URL)
        assert response.url == self.URL

#################### A revoir ?
    def test_request_status_code(self):
        response = WikimediaRequest.request(self.URL)
        assert response.status_code < 300

    @patch('wikimedia_request.requests.get')
    def test_request_bad_status_code(self, mock_get):
        mock_get.return_value.status_code = 404
        response = WikimediaRequest.request(self.URL)
        with pytest.raises(AssertionError):
            assert response.status_code < 300

    @patch('wikimedia_request.requests.get')
    def test_request_is_ok(self, mock_get):
        mock_get.return_value.ok = True
        response = WikimediaRequest.request(self.URL)
        assert response.ok is True

    @patch('wikimedia_request.requests.get')
    def test_request_is_not_ok(self, mock_get):
        mock_get.return_value.ok = False
        response = WikimediaRequest.request(self.URL)
        assert response.ok is False

########################################################

    @patch('wikimedia_request.requests.get')
    def test_request_returns_json(self, mock_get):
        infos = [{"query": {
                    "pages": {
                        "5653202": {
                            "pageid": 5653202,
                            "ns": 0,
                            "title": "Cité Paradis",
                            "extract": "<p class=\"mw-empty-elt\">\n</p>\n"
                                    }
                              }
                            }
        }]
        mock_get.return_value.json.return_value = infos
        response = WikimediaRequest.request(self.URL)
        assert response.json() == infos
