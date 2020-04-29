import os
import requests

from app.API.Gmaps.gmaps_request import GmapsRequest
# from gmaps_request import GmapsRequest

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
            results['error_msg'] = ("Il me semble que cet endroit n'existe "
                                    "pas, pourtant j'ai énormément voyagé..")
            return results
        else:
            results['error_msg'] = ("Une erreur est survenue")
            return results


# obj = GmapsInteraction('OpenClassrooms')
#
# response = obj.get_content()
#
# print(response)
