import requests
import json

class GeoSearchRequest:

    def request(pos):
        try:
            url = str("https://fr.wikipedia.org/w/api.php?action=query&"
            "format=json&list=geosearch&gscoord={0}%7C{1}&gsradius=10000&"
            "gslimit=10".format(pos[0], pos[1]))

            response = requests.get(url, headers={'Content-Type':
                                                  'text/html; charset=utf-8'})
            assert response.status_code < 300

            dict_response = json.loads(response.text)

            return dict_response

        except(AssertionError):
            return ("Problème pour contacter l'API Wikimedia")
        else:
            return ("Une erreur est survenue")
