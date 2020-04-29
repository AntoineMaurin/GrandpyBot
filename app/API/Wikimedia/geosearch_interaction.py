import random

from app.API.Wikimedia.geosearch_request import GeoSearchRequest
# from geosearch_request import GeoSearchRequest

class GeoSearchInteraction:
    def __init__(self, pos):
        self.pos = pos

    def get_page_id(self):
        try:
            response_dict = GeoSearchRequest.request(self.pos)
            pageids = []
            for dict in response_dict["query"]["geosearch"]:
                pageids.append(dict['pageid'])

            return pageids

        except(KeyError):
            return ("Hmm, je ne connais pas grand chose sur cet "
                   "endroit, désolé.")
        else:
            return ("Une erreur est survenue")

obj = GeoSearchInteraction((48.8748465, 2.3504873))
obj.get_page_id()
