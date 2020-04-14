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


    @patch('wikimedia_interaction.WikimediaInteraction.get_content')
    def test_json_response(self, mock_get):
        infos = ['La cité Paradis est une voie publique située dans le']
        mock_get.return_value = infos

        test = WikimediaInteraction(self.TEXT)
        response = test.get_content()
        assert response == infos
