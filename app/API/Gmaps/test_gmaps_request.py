from gmaps_request import GmapsRequest
from unittest.mock import Mock, patch

import pytest, json

from gmaps_request import GmapsRequest

class TestGmapsRequest:

    URL = "http://jsonplaceholder.typicode.com/todos"

    def test_url_attribute(self):
        response = GmapsRequest.request(self.URL)
        assert response.url == self.URL

# à adapter à G-Maps
    @patch('gmaps_request.requests.get')
    def test_get_content(self, mock_get):
        infos = [{
            "userId": 1,
            "id": 1,
            "title": "Do laudry",
            "completed": 'false'
            }]
        mock_get.return_value.json.return_value = infos

        response = GmapsRequest.request(self.URL)

        assert response.json() == infos
