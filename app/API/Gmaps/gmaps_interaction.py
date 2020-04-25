import os
import requests

from app.API.Gmaps.gmaps_request import GmapsRequest
# from gmaps_request import GmapsRequest

class GmapsInteraction:

    def __init__(self, search):
        self.search = search

    def get_content(self):
        try:
            json_response = GmapsRequest.request(self.search)

            results = {}

            address = json_response['results'][0]['formatted_address']
            lat = json_response['results'][0]['geometry']['location']['lat']
            lng = json_response['results'][0]['geometry']['location']['lng']

            results['address'] = address
            results['lat'] = lat
            results['lng'] = lng

            return results

        except(IndexError):
            return ("Lieu introuvable sur Google Maps")
        else:
            return ("Une erreur est survenue")


# obj = GmapsInteraction('Poudlard')
#
# response = obj.get_content()
#
# print(response)
