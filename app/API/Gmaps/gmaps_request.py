from dotenv import load_dotenv

import os
import requests
import json

load_dotenv()

class GmapsRequest:

    def request(search):
        try:
            API_KEY = os.environ['API_KEY']
            url = str("https://maps.googleapis.com/maps/api/place/textsearch"
            "/json?query={}&key={}").format(search, API_KEY)

            response = requests.get(url, headers={'Content-Type':
                                                  'text/html; charset=utf-8'})

            assert response.status_code < 300

            dict_response = json.loads(response.text)

            return dict_response

        except(AssertionError):
            return ("Problème pour contacter l'API Google Places")
        else:
            return ("Une erreur est survenue")

# r = GmapsRequest.request('OpenClassrooms')
# print(r)
# print(type(r))
