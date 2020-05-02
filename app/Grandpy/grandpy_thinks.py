from app.API.Gmaps.gmaps_interaction import GmapsInteraction
from app.API.Wikimedia.geosearch_interaction import GeoSearchInteraction
from app.API.Wikimedia.wikimedia_interaction import WikimediaInteraction

from app.Parser.parser import Parser

from . import precisions

class GrandpyThinks:
    def __init__(self, text):
        self.text = text
        self.response_dict = {}
        self.response_dict['user_text'] = text
        self.response_dict['grandpy_msg'] = ""

    def reflection(self):

        if self.response_dict['user_text'] == '':
            empty_question_msg = ("Bonjour mon petit, tu souhaites savoir"
                                  " l'emplacement de quelque chose ?"
                                  " N'hésites pas à me demander !")
            self.response_dict['user_text'] = "\n"
            self.response_dict['special_text'] = empty_question_msg
            return self.response_dict

        obj = Parser(self.text)
        parser_dict = obj.parse()

        if 'special_text' in parser_dict.keys():
            return self.how_are_you_answer(parser_dict)

        return self.classic_answer(parser_dict)

    def build_infos_dict(self, parser_dict, location_dict):

        geo_search_obj = GeoSearchInteraction((location_dict['lat'],
                                               location_dict['lng']))
        list_ids = geo_search_obj.get_page_id()

        wiki_obj = WikimediaInteraction(list_ids)

        try:
            self.response_dict['address'] = location_dict['address']
            self.response_dict['lat'] = location_dict['lat']
            self.response_dict['lng'] = location_dict['lng']

        except(KeyError):
            msg = ("Hmm il me semble que cela se trouve autour du" +
                   location_dict['address'] + " mais ma mémoire me fait"
                   "défaut, je ne peux pas te montrer l'emplacement exact..")
            self.response_dict['grandpy_msg'] = msg
            return self.response_dict

        # Si demande un lieu avec aucune page wiki alentour
        if len(wiki_obj.error_msg) > 0:
            self.response_dict['grandpy_msg'] = wiki_obj.error_msg
            return self.response_dict

        wiki_dict = wiki_obj.get_content()

        self.response_dict['title'] = wiki_dict['title']
        self.response_dict['text'] = wiki_dict['text']
        self.response_dict['url'] = wiki_dict['url']

    def how_are_you_answer(self, parser_dict):

        gmap = GmapsInteraction(parser_dict["keyword"])
        location_dict = gmap.get_content()
        print(location_dict)

        # if "Comment vas tu papy ?"
        if 'special_text' in parser_dict.keys():
            if 'error_msg' in location_dict.keys():
                self.response_dict['special_text'] = parser_dict['special_text']
                return self.response_dict

        #elif "Comment vas-tu ? Mais où est la tour eiffel ?"
            elif 'error_msg' not in location_dict.keys():

                val = self.build_infos_dict(parser_dict, location_dict)
                if val is not None:
                    msg = ("Je vais très bien, merci. "
                           + self.response_dict['grandpy_msg'])

                    self.response_dict['grandpy_msg'] = msg
                    return self.response_dict

                article = self.get_article()
                special_msg = (" Et pour ta question, cela se trouve au " +
                               self.response_dict['address'] +
                               ", d'ailleurs savais-tu que tout proche se " +
                               article + self.response_dict['title'] + " ? " +
                               self.response_dict['text'] + " ")

            # Réponds : Je vais bien, et ta tour est là
            self.response_dict['grandpy_msg'] = parser_dict['special_text'] + special_msg
            return self.response_dict

    def classic_answer(self, parser_dict):
        gmap = GmapsInteraction(parser_dict["keyword"])
        location_dict = gmap.get_content()

        val = self.build_infos_dict(parser_dict, location_dict)
        if val is not None:
            return self.response_dict

        begin = self.get_begin(parser_dict)
        article = self.get_article()

        msg = (begin + "Cela se trouve au " +
               self.response_dict['address'] +
               ", d'ailleurs savais-tu que tout proche se " +
               article + self.response_dict['title'] + " ? " +
               self.response_dict['text'])

        self.response_dict['grandpy_msg'] = msg

        return self.response_dict

    def get_begin(self, parser_dict):
        begin = ""
        for word in precisions.hello_words:
            if word in parser_dict['initial_text']:
                begin = word.capitalize() + " mon petit ! "
        return begin

    def get_article(self):
        article = ""
        title = self.response_dict['title'].split()[0].lower()
        if title in precisions.masculin:
            article = "trouve le "
        elif title in precisions.feminin:
            article = "trouve la "
        elif title in precisions.pluriel:
            article = "trouvent les "
        elif  title in precisions.apostrophe:
            article = "trouve l'"
        else:
            article = "trouve "
        return article
