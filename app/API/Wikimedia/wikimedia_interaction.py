from app.API.Wikimedia.wikimedia_request import WikimediaRequest

import random
import re

"""This class treats data from a wikipedia page, which is received by the
WikimediaRequest class."""


class WikimediaInteraction:

    def __init__(self, pageids):
        self.error_msg = ""
        try:
            page_id = random.choice(pageids)
            self.search_id = page_id
        except(IndexError):
            self.error_msg = ("Cela se trouve ici, mais je suis désolé, je ne"
                              " connais pas grand chose sur cet endroit..")

    """This method cleans the text in parameter to return it without '=' symbol
    and other undesirable characters that can appear in the result."""
    def clean_data(self, text):
        cleanr = re.compile('=.*?=')
        res = re.sub(cleanr, '', text)
        return res

    """This is the main method of this class, it gets a dictionnary from
    the WikimediaRequest class and adds into another dictionnary the
    content such as the text of the page, the title, and the url.
    Once again, returns an error message if something went wrong."""
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
