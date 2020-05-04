import requests
import json

"""This class sends a GeoSearch request to the media wiki API with a tuple
that contains lattitude and longitude, and it returns a dictionnary with
the wikipedia pages near this location."""


class GeoSearchRequest:

    """This method builds the proper url with the coordinates, transforms
    the json into a dict and returns it, or returns an error message if
    something went wrong."""
    def request(pos):
        try:
            url = str("https://fr.wikipedia.org/w/api.php?action=query&"
                      "format=json&list=geosearch&gscoord={0}%7C{1}"
                      "&gsradius=10000&gslimit=10".format(pos[0], pos[1]))

            response = requests.get(url, headers={'Content-Type':
                                                  'text/html; charset=utf-8'})
            assert response.status_code < 300

            dict_response = json.loads(response.text)

            return dict_response

        except(AssertionError):
            return ("Problème pour contacter l'API Wikimedia")
        else:
            return ("Une erreur est survenue")
