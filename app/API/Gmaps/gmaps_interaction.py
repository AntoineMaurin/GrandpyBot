from dotenv import load_dotenv

import os
import requests
import json

from .gmaps_request import GmapsRequest

load_dotenv()

class GmapsInteraction:

    API_KEY = os.environ['API_KEY']

    def __init__(self, search):
        self.search = search
        self.url = str("https://maps.googleapis.com/maps/api/place/textsearch"
        "/json?query={}&key={}").format(self.search, self.API_KEY)

    def get_content(self):
        response = GmapsRequest.request(self.url)
        json_response = json.loads(response.text)
        results = {'address': None,
                   'lat': None,
                   'lng': None
                   }
        #creusons dans le dictionnaire
        #Il me faut les coordonnées GPS et l'adresse
        address = json_response['results'][0]['formatted_address']
        lat = json_response['results'][0]['geometry']['location']['lat']
        lng = json_response['results'][0]['geometry']['location']['lng']

        #range les résultats
        results['address'] = address
        results['lat'] = lat
        results['lng'] = lng

        return results

        # return json_response["id"]

obj = GmapsInteraction('Mairie de Paris')

response = obj.get_content()

print(response['address'], response['lat'], response['lng'])
