from app.API.Wikimedia.wikimedia_request import WikimediaRequest

import random
import re

class WikimediaInteraction:

    def __init__(self, pageids):
        self.error_msg = ""
        try:
            page_id = random.choice(pageids)
            self.search_id = page_id
        except(IndexError):
            self.error_msg = ("Cela se trouve ici, mais je suis désolé, je ne"
                              " connais pas grand chose sur cet endroit..")

    def clean_data(self, text):
        cleanr = re.compile('=.*?=')
        res = re.sub(cleanr, '', text)
        return res

    def get_content(self):
        try:
            response_dict = {}
            response = WikimediaRequest.request(self.search_id)

            result = response["query"]["pages"][str(self.search_id)]["extract"]
            title = response["query"]["pages"][str(self.search_id)]["title"]

            final_result = " ".join(result.split())

            final_result = final_result[:400] + '... '

            response_dict['text'] = self.clean_data(final_result)
            response_dict['title'] = title
            response_dict['url'] = "https://fr.wikipedia.org/wiki/" + title
            return response_dict

        except(KeyError):
            return ("Hmm, je ne connais pas grand chose sur cet "
                   "endroit, désolé.")
        else:
            return ("Une erreur est survenue")
