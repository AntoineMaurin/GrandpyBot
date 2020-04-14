import requests

class WikimediaRequest:

    @classmethod
    def request(cls, url):
        response = requests.get(url, headers={'Content-Type': 'text/html; charset=utf-8'})
        return response
