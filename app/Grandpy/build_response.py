from . import words

from app.API.Gmaps.gmaps_interaction import GmapsInteraction
from app.API.Wikimedia.geosearch_interaction import GeoSearchInteraction
from app.API.Wikimedia.wikimedia_interaction import WikimediaInteraction
from app.Grandpy.parser import Parser

"""This class builds the response that grandpy says depending on what the
user asked."""


class BuildResponse:

    def __init__(self, user_text):
        self.user_text = user_text

        self.parser_infos = {}
        self.loc_infos = {}
        self.wiki_infos = {}

        self.final_dict = {}
        self.final_dict['user_text'] = user_text

    """This simply returns the final dict when called"""
    def get_response(self):
        final_dict = self.build_final_dict()
        return final_dict

    """This is the main method, it builds step by step the final dict
    depending on what the parser returns, then it takes into account what
    the google maps Places returns and adapt its response and content for
    every possible case."""
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

    """This method builds the dict when all went well."""
    def build_succes_dict(self):
        self.final_dict['lat'] = self.loc_infos['lat']
        self.final_dict['lng'] = self.loc_infos['lng']
        self.final_dict['address'] = self.loc_infos['address']

        self.final_dict['url'] = self.wiki_infos['url']
        self.final_dict['text'] = self.wiki_infos['text']
        self.final_dict['title'] = self.wiki_infos['title']

    """This one builds the 'classic answer', it means the typical message
    returned when you ask a place to granpdy, and there is no problem in
    the operations."""
    def build_classic_answer(self):

        begin, formula = self.get_begin_and_formula()

        msg = (begin + "Cela se trouve au " +
               self.loc_infos['address'] +
               ", d'ailleurs savais-tu que tout proche se " +
               formula + self.wiki_infos['title'] + " ? " +
               self.wiki_infos['text'])
        return msg

    """This method is called when we need to set the location informations
    about the place the parser just found out in the question."""
    def set_loc_infos(self, keyword):
        gmap = GmapsInteraction(keyword)
        self.loc_infos = gmap.get_content()

    """This method is called when we have usable location informations about
    a place, and now we need some wikipedia informations about this place and
    the surronding area."""
    def set_wiki_infos(self, lat, lng, address):
        geo_search_obj = GeoSearchInteraction((lat, lng))
        list_ids = geo_search_obj.get_page_id()

        wiki_obj = WikimediaInteraction(list_ids)

        if len(list_ids) == 0:
            if 'special_text' in self.parser_infos:
                res = (self.parser_infos['special_text'] + wiki_obj.error_msg)
                self.final_dict['grandpy_msg'] = res
            else:
                self.final_dict['grandpy_msg'] = wiki_obj.error_msg

            self.final_dict['lat'] = lat
            self.final_dict['lng'] = lng
            self.final_dict['address'] = address
            return self.final_dict

        self.wiki_infos = wiki_obj.get_content()

    """This method checks if the question is empty, or just don't ask for a
    place to search."""
    def is_empty(self, user_text):
        if user_text.strip() == '':

            empty_question_msg = (" Si tu souhaites savoir"
                                  " l'emplacement de quelque chose,"
                                  " n'hésites pas à me demander !")
            if 'special_text' in self.parser_infos:
                res = (self.parser_infos['special_text'] + empty_question_msg)
                self.final_dict['special_text'] = res

            else:
                self.final_dict['special_text'] = empty_question_msg

            return True

    """This method is here to modify the answer depending of what is in the
    question. If you are hello, how are you, where is this place, it's
    gonna adapt the response here with hey, i'm fine, this is here."""
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
        elif title in words.apostrophe:
            formula = "trouve l'"
        else:
            formula = "trouve "

        return begin, formula
