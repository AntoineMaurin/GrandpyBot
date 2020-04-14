from gmaps_request import GmapsRequest
from unittest.mock import Mock, patch

import pytest, json

class TestGmapsRequest:

    URL = "http://jsonplaceholder.typicode.com/todos"

    def test_request_status_code(self):
        response = GmapsRequest.request(self.URL)
        assert response.status_code < 300

    @patch('gmaps_request.requests.get')
    def test_request_bad_status_code(self, mock_get):
        mock_get.return_value.status_code = 350
        response = GmapsRequest.request(self.URL)
        with pytest.raises(AssertionError):
            assert response.status_code < 300

    @patch('gmaps_request.requests.get')
    def test_request_is_ok(self, mock_get):
        mock_get.return_value.ok = True
        response = GmapsRequest.request(self.URL)
        assert response.ok is True

    @patch('gmaps_request.requests.get')
    def test_request_is_not_ok(self, mock_get):
        mock_get.return_value.ok = False
        response = GmapsRequest.request(self.URL)
        assert response.ok is False

    @patch('gmaps_request.requests.get')
    def test_request_is_ok(self, mock_get):
        infos = [{

        }]
        mock_get.return_value.json.return_value = infos
        response = GmapsRequest.request(self.URL)
        assert response.json() == infos
