import requests
import json

class WikimediaRequest:

    def request(search_id):
        try:
            url = str("https://fr.wikipedia.org/w/api.php?action=query&"
                      "format=json&prop=extracts&pageids={0}&exsentences"
                      "=4&explaintext=1".format(search_id))
            response = requests.get(url, headers={'Content-Type':
                                                  'text/html; charset=utf-8'})

            assert response.status_code < 300

            dict_response = json.loads(response.text)
            return dict_response

        except(AssertionError):
            return ("Problème pour contacter l'API Wikimedia")
        else:
            return ("Une erreur est survenue")
