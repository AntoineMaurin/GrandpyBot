from unittest.mock import Mock, patch

import requests
import re
import json
import pytest

from wikimedia_interaction import WikimediaInteraction

class TestWikimediaInteraction:

    TEXT = "Cité Paradis"

    def test_search_arg(self):
        test = WikimediaInteraction(self.TEXT)
        assert test.search == self.TEXT

    def test_url_type(self):
        test = WikimediaInteraction(self.TEXT)
        assert isinstance(test.url, str)

    def test_url_conversion_type(self):
        test = WikimediaInteraction(142)
        assert isinstance(test.url, str)

    @patch('wikimedia_interaction.WikimediaInteraction.get_content')
    def test_get_content(self, mock_get_content):
        infos = ['La cité Paradis est une voie publique située dans le']
        mock_get_content.return_value = infos

        test = WikimediaInteraction(self.TEXT)
        response = test.get_content()
        assert response == infos
