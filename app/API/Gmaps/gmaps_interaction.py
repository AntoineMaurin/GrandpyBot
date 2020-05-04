from app.API.Gmaps.gmaps_request import GmapsRequest

"""This class is used to treat data from the GmapsRequest class, after
sending it a search."""


class GmapsInteraction:

    def __init__(self, search):
        self.search = search

    """This method uses a dictionnary returned by GmapsRequest class to return
    a new dictionnary that contains informations about the place parameter
    (self.search). In case of an error, returns a custom error message."""
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
            msg = ("Qu'est ce que tu dis ? " + self.search + " ? Je ne connais"
                   " pas ce lieu, ou peut-être ai-je mal compris.. veux-tu"
                   " reformuler s'il te plaît ?")
            results['error_msg'] = str(msg)
            return results
        else:
            results['error_msg'] = "J'en tombe de ma chaise !"
            return results
