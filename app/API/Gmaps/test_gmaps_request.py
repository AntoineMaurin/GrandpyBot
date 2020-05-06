from gmaps_request import GmapsRequest

import json


class TestGmapsRequest:

    TEXT = "OpenClassrooms"

    """Tests in this file are handmade with the class to mock behaviors with
    monkeypatch. Other tests are made with the patch decorator from
    unittest.mock."""
    def test_return_type(self, monkeypatch):
        DATA = {"results": [{
                        "formatted_address": "7 Cité Paradis, 75010 Paris,"
                                             "France",
                        "geometry": {
                          "location": {
                              "lat": 48.8748465,
                              "lng": 2.3504873
                                            }
                                    }
                        }]}

        class MockRequestsGet:
            def __init__(self, url, headers=None):
                self.status_code = 200
                self.text = json.dumps(DATA)

        monkeypatch.setattr('app.API.Gmaps.gmaps_request.requests.get',
                            MockRequestsGet)
        r = GmapsRequest.request(self.TEXT)
        assert isinstance(r, dict)

    def test_type_return_value_when_error(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, headers=None):
                self.status_code = 404

        monkeypatch.setattr('app.API.Gmaps.gmaps_request.requests.get',
                            MockRequestsGet)

        r = GmapsRequest.request(self.TEXT)
        assert isinstance(r, str)

    def test_bad_status_code(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, headers=None):
                self.status_code = 500

        monkeypatch.setattr('app.API.Gmaps.gmaps_request.requests.get',
                            MockRequestsGet)

        response = GmapsRequest.request(self.TEXT)
        assert response == "Problème pour contacter l'API Google Places"
