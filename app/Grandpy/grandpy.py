from . import words

from app.API.Gmaps.gmaps_interaction import GmapsInteraction
from app.API.Wikimedia.geosearch_interaction import GeoSearchInteraction
from app.API.Wikimedia.wikimedia_interaction import WikimediaInteraction
from app.Grandpy.parser import Parser

"""This class builds the response that grandpy says depending on what the
user asked."""


class Grandpy:

    def __init__(self, user_text):
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

        parser = Parser(self.final_dict['user_text'])
        parser_dict = parser.parse()

        if self.is_empty(parser_dict):
            return self.final_dict

        success, loc_result = self.get_loc_infos(parser_dict['keyword'])

        if success is False:
            self.final_dict['special_text'] = loc_result
            return self.final_dict

        success, wiki_result = self.get_wiki_infos(parser_dict,
                                                   loc_result['lat'],
                                                   loc_result['lng'])
        if success is False:
            self.final_dict['lat'] = loc_result['lat']
            self.final_dict['lng'] = loc_result['lng']
            self.final_dict['grandpy_msg'] = wiki_result
            return self.final_dict
        else:
            return self.build_succes_dict(wiki_result, loc_result, parser_dict)

    """This method builds the dict when all went well."""
    def build_succes_dict(self, wiki_dict, loc_infos, parser_dict):
        self.final_dict['lat'] = loc_infos['lat']
        self.final_dict['lng'] = loc_infos['lng']
        self.final_dict['address'] = loc_infos['address']

        self.final_dict['url'] = wiki_dict['url']
        self.final_dict['text'] = wiki_dict['text']
        self.final_dict['title'] = wiki_dict['title']

        self.final_dict['grandpy_msg'] = self.build_classic_answer(wiki_dict,
                                                                   loc_infos,
                                                                   parser_dict)

        return self.final_dict

    """This one builds the 'classic answer', it means the typical message
    returned when you ask a place to granpdy, and there is no problem in
    the operations."""
    def build_classic_answer(self, wiki_dict, loc_infos, parser_dict):

        begin, formula = self.get_begin_and_formula(wiki_dict, parser_dict)

        msg = (begin + "Cela se trouve au " +
               loc_infos['address'] +
               ", d'ailleurs savais-tu que tout proche se " +
               formula + wiki_dict['title'] + " ? " +
               wiki_dict['text'])
        return msg

    """This method is called when we need to set the location informations
    about the place the parser just found out in the question."""
    def get_loc_infos(self, keyword):
        gmap = GmapsInteraction(keyword)
        loc_infos = gmap.get_content()

        if 'error_msg' in loc_infos.keys():
            return False, loc_infos['error_msg']
        else:
            return True, loc_infos

    """This method is called when we have usable location informations about
    a place, and now we need some wikipedia informations about this place and
    the surronding area."""
    def get_wiki_infos(self, parser_dict, lat, lng):
        geo_search_obj = GeoSearchInteraction((lat, lng))
        list_ids = geo_search_obj.get_page_id()

        if len(list_ids) == 0:
            no_page_msg = ("Cela se trouve ici, mais je suis désolé, je ne"
                           " connais pas grand chose sur cet endroit..")
            if 'special_text' in parser_dict:
                res = (parser_dict['special_text'] + no_page_msg)
                return False, res
            else:
                return False, no_page_msg
        else:
            wiki_obj = WikimediaInteraction(list_ids)
            wiki_dict = wiki_obj.get_content()

            return True, wiki_dict

    """This method checks if the question is empty, or just don't ask for a
    place to search."""
    def is_empty(self, parser_dict):
        if parser_dict['keyword'].strip() == '':

            empty_question_msg = (" Si tu souhaites savoir"
                                  " l'emplacement de quelque chose,"
                                  " n'hésites pas à me demander !")
            if 'special_text' in parser_dict:
                res = (parser_dict['special_text'] + empty_question_msg)
                self.final_dict['special_text'] = res

            else:
                self.final_dict['special_text'] = empty_question_msg

            return True

    """This method is here to modify the answer depending of what is in the
    question. If you are hello, how are you, where is this place, it's
    gonna adapt the response here with hey, i'm fine, this is here."""
    def get_begin_and_formula(self, wiki_dict, parser_dict):
        if 'special_text' in parser_dict:
            begin = parser_dict['special_text']
        else:
            begin = "Bien sûr mon poussin ! "

        formula = ""
        title = wiki_dict['title'].split()[0].lower()
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
