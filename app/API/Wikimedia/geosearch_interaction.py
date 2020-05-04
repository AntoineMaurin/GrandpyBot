from app.API.Wikimedia.geosearch_request import GeoSearchRequest

"""This class interacts with the GeoSearch request made by the GeoSearchRequest
class and returns a list of page ids in its main function."""


class GeoSearchInteraction:
    def __init__(self, pos):
        self.pos = pos

    """This method gets a dictionnary from the GeoSearchRequest class and
    returns the list of page ids, or an error message if something went
    wrong."""

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
