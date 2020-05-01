from unittest.mock import Mock, patch

import requests
import re
import json
import pytest

from wikimedia_interaction import WikimediaInteraction
from wikimedia_request import WikimediaRequest

class TestWikimediaInteraction:

    IDS = [5653202]
    WIKI_DICT = {"query": {
                    "pages": {
                        "5653202": {
                        "pageid": 5653202,
                        "ns": 0,
                        "title": "Cité Paradis",
                        "extract": "La cité Paradis est une voie publique "
                                    }
                            }
                        }
                }

    def test_search_attr(self):
        obj = WikimediaInteraction(self.IDS)
        assert obj.search_id in self.IDS

    def test_search_attr_type(self):
        obj = WikimediaInteraction(self.IDS)
        assert isinstance(obj.search_id, int)

    @patch('app.API.Wikimedia.wikimedia_request.WikimediaRequest.request')
    def test_get_content_text(self, mock_dict):

        mock_dict.return_value = self.WIKI_DICT

        obj = WikimediaInteraction(self.IDS)
        response = obj.get_content()
        assert response['text'] == "La cité Paradis est une voie publique... "


    @patch('app.API.Wikimedia.wikimedia_request.WikimediaRequest.request')
    def test_get_content_title(self, mock_dict):

        mock_dict.return_value = self.WIKI_DICT

        obj = WikimediaInteraction(self.IDS)
        response = obj.get_content()
        assert response['title'] == "Cité Paradis"

    @patch('app.API.Wikimedia.wikimedia_request.WikimediaRequest.request')
    def test_get_content_url(self, mock_dict):

        mock_dict.return_value = self.WIKI_DICT

        obj = WikimediaInteraction(self.IDS)
        response = obj.get_content()
        assert response['url'] == "https://fr.wikipedia.org/wiki/Cité Paradis"

    def test_get_clean_data(self):
        entry_data = ("La cité Paradis est une voie publique située dans"
                      "le 10e arrondissement de Paris."
                      "== Situation et accès =="
                      "La cité Paradis est une voie publique.")

        obj = WikimediaInteraction(self.IDS)
        response = obj.clean_data(entry_data)
        assert response == ("La cité Paradis est une voie publique située"
                            " dansle 10e arrondissement de Paris. Situation"
                            " et accès La cité Paradis est une voie publique.")


    @patch('app.API.Wikimedia.wikimedia_request.WikimediaRequest.request')
    def test_key_error(self, mock_bad_key):
        bad_dict = {"unknown_key": {
                        "pages": {
                            "5653202": {
                            "pageid": 5653202,
                            "ns": 0,
                            "title": "Cité Paradis",
                            "extract": "La cité Paradis est une voie publique "
                                        }
                                }
                            }
                    }
        mock_bad_key.return_value = bad_dict
        obj = WikimediaInteraction(self.IDS)
        response = obj.get_content()
        assert response == ("Hmm, je ne connais pas grand chose sur "
                            "cet endroit, désolé.")
