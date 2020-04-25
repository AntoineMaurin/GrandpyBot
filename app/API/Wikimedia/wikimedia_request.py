import requests
import json

class WikimediaRequest:

    def request(search):
        try:
            url = str("https://fr.wikipedia.org/w/api.php"
            "?action=query&format=json&prop=extracts&titles={0}"
            "&redirects=1&exsentences=4&explaintext=1".format(search))

            response = requests.get(url, headers={'Content-Type':
                                                  'text/html; charset=utf-8'})

            assert response.status_code < 300

            dict_response = json.loads(response.text)

            return dict_response

        except(AssertionError):
            return ("Problème pour contacter l'API Wikimedia")


# resp = WikimediaRequest.request('Cité Paradis')
#
# resp.blabla = 404
# print(resp)
# print(resp.blabla)
