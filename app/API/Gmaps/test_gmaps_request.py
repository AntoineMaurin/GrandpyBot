from gmaps_request import GmapsRequest


class TestGmapsRequest:

    TEXT = "OpenClassrooms"
    DATA = {"results": [{
                    "formatted_address": "7 Cité Paradis, 75010 Paris, France",
                    "geometry": {
                      "location": {
                          "lat": 48.8748465,
                          "lng": 2.3504873
                                        }
                                }
                    }]}

    def test_type_return_value_when_error(self, monkeypatch):
        class MockRequestsStatusCode:
            def __init__(self, url, headers):
                self.status_code = 404

        monkeypatch.setattr('app.API.Gmaps.gmaps_request.requests.get',
                            MockRequestsStatusCode)

        r = GmapsRequest.request(self.TEXT)
        assert isinstance(r, str)

    def test_bad_status_code(self, monkeypatch):
        class MockRequestsStatusCode:
            def __init__(self, url, headers):
                self.status_code = 500

        monkeypatch.setattr('app.API.Gmaps.gmaps_request.requests.get',
                            MockRequestsStatusCode)

        response = GmapsRequest.request(self.TEXT)
        assert response == "Problème pour contacter l'API Google Places"
