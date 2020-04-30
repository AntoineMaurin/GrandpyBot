from app.API.Gmaps.gmaps_interaction import GmapsInteraction
from app.API.Wikimedia.geosearch_interaction import GeoSearchInteraction
from app.API.Wikimedia.wikimedia_interaction import WikimediaInteraction

from app.Parser.parser import Parser

from . import titles

class GrandpyThinks:
    def __init__(self, text):
        self.text = text
        self.response_dict = {}
        self.response_dict['user_text'] = text

    def reflection(self):
        obj = Parser(self.text)
        keyword = obj.parse()

        gmap = GmapsInteraction(keyword)
        location_dict = gmap.get_content()

        if 'error_msg' in location_dict.keys():
            self.response_dict['error_msg'] = location_dict['error_msg']
            return self.response_dict

        else:
            geo_search_obj = GeoSearchInteraction((location_dict['lat'],
                                                   location_dict['lng']))
            list_ids = geo_search_obj.get_page_id()
            wiki_obj = WikimediaInteraction(list_ids)
            wiki_response_dict = wiki_obj.get_content()

            self.response_dict['address'] = location_dict['address']
            self.response_dict['lat'] = location_dict['lat']
            self.response_dict['lng'] = location_dict['lng']
            self.response_dict['title'] = wiki_response_dict['title']
            self.response_dict['text'] = wiki_response_dict['text']
            self.response_dict['url'] = wiki_response_dict['url']

            return self.build_answer()

    def build_answer(self):

        title = self.response_dict['title'].split()[0].lower()
        if title in titles.masculin:
            article = "trouve le "
        elif title in titles.feminin:
            article = "trouve la "
        elif title in titles.pluriel:
            article = "trouvent les "
        elif  title in titles.apostrophe:
            article = "trouve l'"
        else:
            article = "trouve "

        self.response_dict['grandpy_msg'] = ("Cela se trouve au " + self.response_dict['address'] +
                                             ", d'ailleurs savais-tu que tout proche se " +
                                             article + self.response_dict['title'] + " ? " +
                                             self.response_dict['text'])
        return self.response_dict
