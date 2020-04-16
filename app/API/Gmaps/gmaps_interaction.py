import requests
import json

from gmaps_request import GmapsRequest

class GmapsInteraction:

    def __init__(self, search):
        self.search = search
        self.url = str("http://jsonplaceholder.typicode.com/{}").format(self.search)

    def get_content(self):
        response = GmapsRequest.request(self.url)
        json_response = json.loads(response.text)

        #creusons dans le dictionnaire
        #Il me faudrait les coordonnées GPS et l'adresse
        l = []
        for i in range(15):
            l.append(json_response[i]["title"])
        #range les résultats

        return l

        # return json_response["id"]

obj = GmapsInteraction('todos')

response = obj.get_content()

print(response)
