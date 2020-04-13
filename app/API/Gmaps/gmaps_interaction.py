import requests
import json

class GmapsInteraction:

    def __init__(self):
        self.url = "http://jsonplaceholder.typicode.com/todos"

    def request(self):

        response = requests.get(self.url)
        self.status_code = response.status_code

        if response.ok:
            return response
        else:
            return None

    def get_json_response(self):
        reponse = self.request()
        json_response = json.loads(response.text)

        return json_response
