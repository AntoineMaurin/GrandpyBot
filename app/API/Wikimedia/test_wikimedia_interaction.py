from unittest.mock import Mock, patch

import requests
import re
import json
import pytest

from wikimedia_interaction import WikimediaInteraction
from wikimedia_request import WikimediaRequest

class TestWikimediaInteraction:

    TEXT = "Cité Paradis"

    def test_search_attr(self):
        obj = WikimediaInteraction(self.TEXT)
        assert self.TEXT == obj.search

    def test_search_attr_fails(self):
        obj = WikimediaInteraction(self.TEXT)
        with pytest.raises(AssertionError):
            assert not self.TEXT == obj.search

    @patch('app.API.Wikimedia.wikimedia_request.WikimediaRequest.request')
    def test_get_content(self, mock_dict):
        wiki_dict = {"query": {
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
        mock_dict.return_value = wiki_dict

        obj = WikimediaInteraction(self.TEXT)
        response = obj.get_content()

        assert response == "La cité Paradis est une voie publique"

    @patch('app.API.Wikimedia.wikimedia_request.WikimediaRequest.request')
    def test_get_content_fails(self, mock_dict):
        wiki_dict = {"query": {
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
        mock_dict.return_value = wiki_dict

        obj = WikimediaInteraction(self.TEXT)
        response = obj.get_content()

        with pytest.raises(AssertionError):
            assert not response == "La cité Paradis est une voie publique"

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
        obj = WikimediaInteraction(self.TEXT)
        response = obj.get_content()
        assert response == 'Pas de résultat sur wikipédia'
