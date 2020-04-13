import requests
import json
import re

class WikimediaInteraction:

    def __init__(self, search):
        self.search = search
        self.url = "https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={}&redirects=1&exsentences=4".format(self.search)
        self.status_code = ''

    def request(self):
        response = requests.get(self.url, headers={'Content-Type': 'text/html; charset=utf-8'})
        self.status_code = response.status_code
        return response

    def get_json_response(self):
        response = self.request()
        json_response = json.loads(response.text)
        return json_response

    def get_extract_field(self):

        json_response = self.get_json_response()

        for key in json_response["query"]["pages"]:
            keyid = key
        result = json_response["query"]["pages"][keyid]["extract"]

        return result

    def cleanhtml(self, raw_html):
        clean = re.compile('<.*?>')
        clean_result = re.sub(clean, '', raw_html)
        return clean_result


interact = WikimediaInteraction('Cité Paradis')

result = interact.get_extract_field()
print('result : ', result)

final_text = interact.cleanhtml(result)
print('final_text : ', final_text)
