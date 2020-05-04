from . import words

from app.API.Gmaps.gmaps_interaction import GmapsInteraction
from app.API.Wikimedia.geosearch_interaction import GeoSearchInteraction
from app.API.Wikimedia.wikimedia_interaction import WikimediaInteraction
from app.Grandpy.parser import Parser

class BuildResponse:

    def __init__(self, user_text):
        self.user_text = user_text

        # has {'initial_text', 'hello_text', 'special_text', 'keyword'}
        self.parser_infos = {}
        self.loc_infos = {}
        self.wiki_infos = {}

        self.final_dict = {}
        self.final_dict['user_text'] = user_text

    # Returns dict {'user_text', 'grandpy_msg', 'special_text', 'url'}
    def get_response(self):
        final_dict = self.build_final_dict()
        return final_dict

    def build_final_dict(self):

        parser = Parser(self.user_text)
        self.parser_infos = parser.parse()

        if self.is_empty(self.parser_infos['keyword']):
            return self.final_dict

        self.set_loc_infos(self.parser_infos['keyword'])

        if 'error_msg' in self.loc_infos:
            self.final_dict['special_text'] = self.loc_infos['error_msg']
            return self.final_dict

        end = self.set_wiki_infos(self.loc_infos['lat'],
                                  self.loc_infos['lng'],
                                  self.loc_infos['address'])
        if end is not None:
            return self.final_dict
        else:
            self.build_succes_dict()
            grandpy_msg = self.build_classic_answer()

            self.final_dict['grandpy_msg'] = grandpy_msg
            return self.final_dict

    def build_succes_dict(self):
        self.final_dict['lat'] = self.loc_infos['lat']
        self.final_dict['lng'] = self.loc_infos['lng']
        self.final_dict['address'] = self.loc_infos['address']

        self.final_dict['url'] = self.wiki_infos['url']
        self.final_dict['text'] = self.wiki_infos['text']
        self.final_dict['title'] = self.wiki_infos['title']

    def build_classic_answer(self):

        begin, formula = self.get_begin_and_formula()

        msg = (begin + "Cela se trouve au " +
               self.loc_infos['address'] +
               ", d'ailleurs savais-tu que tout proche se " +
               formula + self.wiki_infos['title'] + " ? " +
               self.wiki_infos['text'])
        return msg

    def set_loc_infos(self, keyword):
        gmap = GmapsInteraction(keyword)
        self.loc_infos = gmap.get_content()

    def set_wiki_infos(self, lat, lng, address):
        geo_search_obj = GeoSearchInteraction((lat, lng))
        list_ids = geo_search_obj.get_page_id()

        wiki_obj = WikimediaInteraction(list_ids)

        if len(list_ids) == 0:
            if 'special_text' in self.parser_infos:
                self.final_dict['grandpy_msg'] = (self.parser_infos['special_text'] +
                                                  wiki_obj.error_msg)
            else:
                self.final_dict['grandpy_msg'] = wiki_obj.error_msg

            self.final_dict['lat'] = lat
            self.final_dict['lng'] = lng
            self.final_dict['address'] = address
            return self.final_dict

        self.wiki_infos = wiki_obj.get_content()

    def is_empty(self, user_text):
        empty_case_dict = {}
        if user_text.strip() == '':

            empty_question_msg = (" Si tu souhaites savoir"
                                  " l'emplacement de quelque chose,"
                                  " n'hésites pas à me demander !")
            if 'special_text' in self.parser_infos:
                self.final_dict['special_text'] = (self.parser_infos['special_text']
                                                   + empty_question_msg)
            else:
                self.final_dict['special_text'] = empty_question_msg

            return True

    def get_begin_and_formula(self):
        if 'special_text' in self.parser_infos:
            begin = self.parser_infos['special_text']
        else:
            begin = "Bien sûr mon poussin ! "

        formula = ""
        title = self.wiki_infos['title'].split()[0].lower()
        if title in words.masculin:
            formula = "trouve le "
        elif title in words.feminin:
            formula = "trouve la "
        elif title in words.pluriel:
            formula = "trouvent les "
        elif  title in words.apostrophe:
            formula = "trouve l'"
        else:
            formula = "trouve "

        return begin, formula
