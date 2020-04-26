from app.API.Wikimedia.wikimedia_request import WikimediaRequest
# from wikimedia_request import WikimediaRequest

class WikimediaInteraction:

    def __init__(self, search):
        self.search = search

    def get_content(self):
        try:
            response = WikimediaRequest.request(self.search)

            for key in response["query"]["pages"]:
                keyid = key
            result = response["query"]["pages"][keyid]["extract"]

            final_result = " ".join(result.split())

            return final_result

        except(KeyError):
            return ("Hmm, {} je ne connais pas grand chose sur cet "
                   "endroit, désolé.".format(self.search))
        else:
            return ("Une erreur est survenue")


# interact = WikimediaInteraction("Cité Paradis")
#
# result = interact.get_content()
# print(result)
