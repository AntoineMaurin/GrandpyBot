from app.API.Wikimedia.wikimedia_request import WikimediaRequest
from unittest.mock import patch


class TestWikimediaRequest:

    TEXT = "Cité Paradis"
    DATA = '{"extract": "La cité Paradis est une voie publique..."}'

    @patch('app.API.Wikimedia.wikimedia_request.requests.get')
    def setup_function(self, mock_text):
        mock_text.return_value.text = self.DATA

    def test_dict_tranform(self):
        r = WikimediaRequest.request(self.TEXT)
        assert isinstance(r, dict)

    @patch('app.API.Wikimedia.wikimedia_request.requests.get')
    def test_return_value_when_error(self, mock_bad_status_code):
        mock_bad_status_code.return_value.status_code = 404
        r = WikimediaRequest.request(self.TEXT)
        assert isinstance(r, str)

    @patch('app.API.Wikimedia.wikimedia_request.requests.get')
    def test_bad_status_code(self, mock_bad_status_code):
        mock_bad_status_code.return_value.status_code = 404
        response = WikimediaRequest.request(self.TEXT)
        assert response == "Problème pour contacter l'API Wikimedia"
