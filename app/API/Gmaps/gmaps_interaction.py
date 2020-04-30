import os
import requests

from app.API.Gmaps.gmaps_request import GmapsRequest

class GmapsInteraction:

    def __init__(self, search):
        self.search = search

    def get_content(self):
        results = {}
        try:
            json_response = GmapsRequest.request(self.search)

            address = json_response['results'][0]['formatted_address']
            lat = json_response['results'][0]['geometry']['location']['lat']
            lng = json_response['results'][0]['geometry']['location']['lng']

            results['address'] = address
            results['lat'] = lat
            results['lng'] = lng

            return results

        except(IndexError):
            results['error_msg'] = ("Je n'ai pas bien compris ta question, "
                                    "veux-tu reformuler s'il te plaît ?")
            return results
        else:
            results['error_msg'] = ("Une erreur est survenue")
            return results
