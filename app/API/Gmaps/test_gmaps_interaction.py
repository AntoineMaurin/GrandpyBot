from unittest.mock import Mock, patch

import requests
import json

from gmaps_interaction import GmapsInteraction

class TestGmapsInteraction:

    TEXT = "OpenClassrooms"

    def test_search_arg(self):
        test = GmapsInteraction(self.TEXT)
        assert test.search == self.TEXT

    def test_url_type(self):
        test = GmapsInteraction(self.TEXT)
        assert isinstance(test.url, str)

    def test_url_conversion_type(self):
        test = GmapsInteraction(142)
        assert isinstance(test.url, str)

    @patch('gmaps_interaction.GmapsInteraction.get_content')
    def test_get_content(self, mock_get_content):
        infos = ('6 Cité Paradis, 75010 Paris', 33.501, 28.904)
        mock_get_content.return_value = infos

        test = GmapsInteraction(self.TEXT)
        response = test.get_content()
        assert response == infos

# Test transmission des données à la classe API Wiki
