from unittest.mock import Mock, patch

import requests
import re
import json
import pytest

from geosearch_interaction import GeoSearchInteraction
from geosearch_request import GeoSearchRequest

class TestGeoSearchInteraction:

    POS = (48.8748465, 2.3504873)
    DATA = {
            "batchcomplete": "",
            "query": {
                "geosearch": [
                        {
                        "pageid": 5653202,
                        "ns": 0,
                        "title": "Cité Paradis",
                        "lat": 48.87409,
                        "lon": 2.35064,
                        "dist": 84.9,
                        "primary": ""
                        },
                        {
                        "pageid": 6035646,
                        "ns": 0,
                        "title": "Hôtel Botterel de Quintin",
                        "lat": 48.8742,
                        "lon": 2.34989,
                        "dist": 84.1,
                        "primary": ""
                        }
                    ]
                }
            }

    def test_pos_attr(self):
        obj = GeoSearchInteraction(self.POS)
        assert obj.pos == self.POS

    def test_pos_attr_type(self):
        obj = GeoSearchInteraction(self.POS)
        assert isinstance(obj.pos, tuple)

    @patch('app.API.Wikimedia.geosearch_request.GeoSearchRequest.request')
    def test_get_content_text(self, mock_dict):

        mock_dict.return_value = self.DATA

        obj = GeoSearchInteraction(self.POS)
        response = obj.get_page_id()
        assert response == [5653202, 6035646]

    @patch('app.API.Wikimedia.geosearch_request.GeoSearchRequest.request')
    def test_get_content_text(self, mock_dict):

        mock_dict.return_value = self.DATA

        obj = GeoSearchInteraction(self.POS)
        response = obj.get_page_id()
        pageids = []
        for dict in self.DATA["query"]["geosearch"]:
            pageids.append(dict['pageid'])
        assert response == pageids


    @patch('app.API.Wikimedia.geosearch_request.GeoSearchRequest.request')
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
        obj = GeoSearchInteraction(self.POS)
        response = obj.get_page_id()
        assert response == ("Hmm, je ne connais pas grand chose sur "
                            "cet endroit, désolé.")
