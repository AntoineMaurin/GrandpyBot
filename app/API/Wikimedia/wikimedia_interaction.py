import json

from .wikimedia_request import WikimediaRequest
from .clean_data import CleanData

class WikimediaInteraction:

    def __init__(self, search):
        self.search = search
        self.url = str("https://fr.wikipedia.org/w/api.php"
        "?action=query&format=json&prop=extracts&titles={0}"
        "&redirects=1&exsentences=4&explaintext=1".format(self.search))

    def get_content(self):
        response = WikimediaRequest.request(self.url)

        json_response = json.loads(response.text)

        for key in json_response["query"]["pages"]:
            keyid = key
        result = json_response["query"]["pages"][keyid]["extract"]

        final_result = CleanData.clean(result)

        return final_result


interact = WikimediaInteraction("Rue de Rivoli")

result = interact.get_content()
print(result)
