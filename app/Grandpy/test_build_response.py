from app.Grandpy.build_response import BuildResponse
from unittest.mock import Mock, patch

import pytest

from app.Grandpy import words

class TestBuildResponse:

    TEXT = ["",
            "        ",
            "Bonjour !",
            "Bonjour Grandpy, comment ça va ?",
            "Bonjour GrandPy ! Est-ce que tu connais l'adresse"
            " d'OpenClassrooms ?",
            "Hello mon robot, la forme ? Connais-tu l'emplacement de la"
            "tour de pise par hasard ?",
            "Dis grandpy, que peux-tu me dire sur le groenland ?",
            "Coucou ! Est ce que tu saurais où se trouve Poudlard ?"
            ]

    def test_user_text(self):
        obj = BuildResponse(self.TEXT[3])
        test_dict = obj.get_response()
        assert obj.final_dict['user_text'] == self.TEXT[3]

    def test_get_response(self):
        obj = BuildResponse(self.TEXT[0])
        assert isinstance(obj.get_response(), dict)

    def test_empty_question(self):
        empty_question_msg = (" Si tu souhaites savoir"
                              " l'emplacement de quelque chose,"
                              " n'hésites pas à me demander !")

        for i, j in enumerate(self.TEXT[:2]):
            obj = BuildResponse(self.TEXT[i])
            assert obj.get_response()['special_text'] == empty_question_msg

    def test_hello_in_question(self):
        for i, j in enumerate(self.TEXT[2:4]):
            obj = BuildResponse(j)
            assert 'Bonjour' in obj.get_response()['special_text']

    def test_how_are_you_in_question(self):
        obj = BuildResponse(self.TEXT[3])
        imfine = "Et bien ma foi, je suis en pleine forme aujourd'hui ! "
        assert imfine in obj.get_response()['special_text']

    @patch('app.API.Wikimedia.wikimedia_interaction.WikimediaInteraction.get_content')
    @patch('app.API.Wikimedia.geosearch_interaction.GeoSearchInteraction.get_page_id')
    @patch('app.API.Gmaps.gmaps_interaction.GmapsInteraction.get_content')
    def test_hello_if_found_place(self, mock_gmap, mock_geos, mock_wiki):
        gmap_response = {'address': '7 Cité Paradis, 75010 Paris, France',
                        'lat':  48.8748465,
                        'lng': 2.3504873
                        }
        geosearch_response = [3504931, 5475546, 5653202, 6035646]
        wiki_resp = {'text': "La cité d'Hauteville est une voie du 10e "
                             "arrondissement de Paris, en France. Situation"
                             " et accès La cité d'Hauteville est une voie"
                             " publique située dans le 10e arrondissement"
                             " de Paris. Elle débute au 82, rue "
                             "d'Hauteville et se termine au 51...",
                    'title': "Cité d'Hauteville",
                    'url': ("https://fr.wikipedia.org/wiki/"
                            "Cit%C3%A9_d%27Hauteville"),
                    }
        mock_gmap.return_value = gmap_response
        mock_geos.return_value = geosearch_response
        mock_wiki.return_value = wiki_resp

        for i, j in enumerate(self.TEXT):
            obj = BuildResponse(self.TEXT[i])
            test_dict = obj.get_response()
            for w in words.hello_words:
                if w in test_dict['user_text'].lower():
                    if 'grandpy_msg' in test_dict.keys():
                        assert ((w.capitalize() + " la jeunesse ! ") in
                                 test_dict['grandpy_msg'])
                    elif 'special_text' in test_dict.keys():
                        assert ((w.capitalize() + " la jeunesse ! ") in
                                 test_dict['special_text'])

    @patch('app.API.Wikimedia.geosearch_interaction.GeoSearchInteraction.get_page_id')
    @patch('app.API.Gmaps.gmaps_interaction.GmapsInteraction.get_content')
    def test_hello_if_found_place_no_info(self, mock_gmap, mock_geos):
        gmap_response = {'address': '7 Cité Paradis, 75010 Paris, France',
                        'lat':  48.8748465,
                        'lng': 2.3504873
                        }
        geosearch_response = []

        mock_gmap.return_value = gmap_response
        mock_geos.return_value = geosearch_response

        for i, j in enumerate(self.TEXT):
            obj = BuildResponse(self.TEXT[i])
            test_dict = obj.get_response()
            for w in words.hello_words:
                if w in test_dict['user_text'].lower():
                    if 'grandpy_msg' in test_dict.keys():
                        assert ((w.capitalize() + " la jeunesse ! ") in
                                 test_dict['grandpy_msg'])
                    elif 'special_text' in test_dict.keys():
                        assert ((w.capitalize() + " la jeunesse ! ") in
                                 test_dict['special_text'])

    @patch('app.API.Wikimedia.wikimedia_interaction.WikimediaInteraction.get_content')
    @patch('app.API.Wikimedia.geosearch_interaction.GeoSearchInteraction.get_page_id')
    @patch('app.API.Gmaps.gmaps_interaction.GmapsInteraction.get_content')
    def test_imfine_if_found_place(self, mock_gmap, mock_geos, mock_wiki):
        gmap_response = {'address': '7 Cité Paradis, 75010 Paris, France',
                        'lat':  48.8748465,
                        'lng': 2.3504873
                        }
        geosearch_response = [3504931, 5475546, 5653202, 6035646]
        wiki_resp = {'text': "La cité d'Hauteville est une voie du 10e "
                             "arrondissement de Paris, en France. Situation"
                             " et accès La cité d'Hauteville est une voie"
                             " publique située dans le 10e arrondissement"
                             " de Paris. Elle débute au 82, rue "
                             "d'Hauteville et se termine au 51...",
                    'title': "Cité d'Hauteville",
                    'url': ("https://fr.wikipedia.org/wiki/"
                            "Cit%C3%A9_d%27Hauteville"),
                    }
        mock_gmap.return_value = gmap_response
        mock_geos.return_value = geosearch_response
        mock_wiki.return_value = wiki_resp

        sentence = "Et bien ma foi, je suis en pleine forme aujourd'hui ! "

        for i, j in enumerate(self.TEXT):
            obj = BuildResponse(self.TEXT[i])
            test_dict = obj.get_response()
            for w in words.how_are_you:
                if w in test_dict['user_text'].lower():
                    if 'grandpy_msg' in test_dict.keys():
                        assert sentence in test_dict['grandpy_msg']
                    elif 'special_text' in test_dict.keys():
                        assert sentence in test_dict['special_text']

    @patch('app.API.Wikimedia.geosearch_interaction.GeoSearchInteraction.get_page_id')
    @patch('app.API.Gmaps.gmaps_interaction.GmapsInteraction.get_content')
    def test_imfine_if_found_place_no_info(self, mock_gmap, mock_geos):
        gmap_response = {'address': '7 Cité Paradis, 75010 Paris, France',
                        'lat':  48.8748465,
                        'lng': 2.3504873
                        }
        geosearch_response = []

        mock_gmap.return_value = gmap_response
        mock_geos.return_value = geosearch_response

        sentence = "Et bien ma foi, je suis en pleine forme aujourd'hui ! "

        for i, j in enumerate(self.TEXT):
            obj = BuildResponse(self.TEXT[i])
            test_dict = obj.get_response()
            for w in words.how_are_you:
                if w in test_dict['user_text'].lower():
                    if 'grandpy_msg' in test_dict.keys():
                        assert sentence in test_dict['grandpy_msg']
                    elif 'special_text' in test_dict.keys():
                        assert sentence in test_dict['special_text']

    @patch('app.API.Wikimedia.wikimedia_interaction.WikimediaInteraction.get_content')
    @patch('app.API.Wikimedia.geosearch_interaction.GeoSearchInteraction.get_page_id')
    @patch('app.API.Gmaps.gmaps_interaction.GmapsInteraction.get_content')
    def test_grandpy_msg_if_found_place(self, mock_gmap, mock_geos, mock_wiki):
        gmap_response = {'address': '7 Cité Paradis, 75010 Paris, France',
                        'lat':  48.8748465,
                        'lng': 2.3504873
                         }
        geosearch_response = [3504931, 5475546, 5653202, 6035646]
        wiki_resp = {'text': ("La cité d'Hauteville est une voie du 10e "
                             "arrondissement de Paris, en France. Situation"
                             " et accès La cité d'Hauteville est une voie"
                             " publique située dans le 10e arrondissement"
                             " de Paris. Elle débute au 82, rue "
                             "d'Hauteville et se termine au 51..."),
                    'title': "Cité d'Hauteville",
                    'url': ("https://fr.wikipedia.org/wiki/"
                            "Cit%C3%A9_d%27Hauteville"),
                     }
        mock_gmap.return_value = gmap_response
        mock_geos.return_value = geosearch_response
        mock_wiki.return_value = wiki_resp

        expected_msg = ("Bonjour la jeunesse ! Cela se trouve au 7 Cité "
                        "Paradis, 75010 Paris, France, d'ailleurs savais-tu "
                        "que tout proche se trouve la Cité d'Hauteville ? La "
                        "cité d'Hauteville est une voie du 10e arrondissement "
                        "de Paris, en France. Situation et accès La cité "
                        "d'Hauteville est une voie publique située dans le 10e"
                        " arrondissement de Paris. Elle débute au 82, rue "
                        "d'Hauteville et se termine au 51...")

        obj = BuildResponse(self.TEXT[4])
        test_dict = obj.get_response()
        assert test_dict['grandpy_msg'] == expected_msg

    @patch('app.API.Wikimedia.geosearch_interaction.GeoSearchInteraction.get_page_id')
    @patch('app.API.Gmaps.gmaps_interaction.GmapsInteraction.get_content')
    def test_grandpy_msg_if_found_place_no_info(self, mock_gmap, mock_geos):
        gmap_response = {'address': '7 Cité Paradis, 75010 Paris, France',
                        'lat':  48.8748465,
                        'lng': 2.3504873
                         }
        geosearch_response = []
        mock_gmap.return_value = gmap_response
        mock_geos.return_value = geosearch_response

        expected_msg = ("Bonjour la jeunesse ! Cela se trouve ici, mais"
                        " je suis désolé, je ne connais pas grand chose sur"
                        " cet endroit..")

        obj = BuildResponse(self.TEXT[4])
        test_dict = obj.get_response()
        assert test_dict['grandpy_msg'] == expected_msg

    @patch('app.API.Wikimedia.geosearch_interaction.GeoSearchInteraction.get_page_id')
    @patch('app.API.Gmaps.gmaps_interaction.GmapsInteraction.get_content')
    def test_coords_if_found_place_no_info(self, mock_gmap, mock_geos):
        gmap_response = {'address': '7 Cité Paradis, 75010 Paris, France',
                        'lat':  48.8748465,
                        'lng': 2.3504873
                         }
        geosearch_response = []
        mock_gmap.return_value = gmap_response
        mock_geos.return_value = geosearch_response

        expected_msg = ("Bonjour la jeunesse ! Cela se trouve ici, mais"
                        " je suis désolé, je ne connais pas grand chose sur"
                        " cet endroit..")

        obj = BuildResponse(self.TEXT[4])
        test_dict = obj.get_response()
        assert test_dict['lat'] == 48.8748465 and test_dict['lng'] == 2.3504873

    @patch('app.API.Wikimedia.wikimedia_interaction.WikimediaInteraction.get_content')
    @patch('app.API.Wikimedia.geosearch_interaction.GeoSearchInteraction.get_page_id')
    @patch('app.API.Gmaps.gmaps_interaction.GmapsInteraction.get_content')
    def test_url_if_found_place(self, mock_gmap, mock_geos, mock_wiki):
        gmap_response = {'address': '7 Cité Paradis, 75010 Paris, France',
                        'lat':  48.8748465,
                        'lng': 2.3504873
                        }
        geosearch_response = [3504931, 5475546, 5653202, 6035646]
        wiki_resp = {'text': ("La cité d'Hauteville est une voie du 10e "
                             "arrondissement de Paris, en France. Situation"
                             " et accès La cité d'Hauteville est une voie"
                             " publique située dans le 10e arrondissement"
                             " de Paris. Elle débute au 82, rue "
                             "d'Hauteville et se termine au 51..."),
                    'title': "Cité d'Hauteville",
                    'url': ("https://fr.wikipedia.org/wiki/"
                            "Cit%C3%A9_d%27Hauteville"),
                    }
        mock_gmap.return_value = gmap_response
        mock_geos.return_value = geosearch_response
        mock_wiki.return_value = wiki_resp


        obj = BuildResponse(self.TEXT[4])
        test_dict = obj.get_response()
        assert test_dict['url'] == ("https://fr.wikipedia.org/wiki/"
                                    "Cit%C3%A9_d%27Hauteville")

    @patch('app.API.Wikimedia.wikimedia_interaction.WikimediaInteraction.get_content')
    @patch('app.API.Wikimedia.geosearch_interaction.GeoSearchInteraction.get_page_id')
    @patch('app.API.Gmaps.gmaps_interaction.GmapsInteraction.get_content')
    def test_coords_if_found_place(self, mock_gmap, mock_geos, mock_wiki):
        gmap_response = {'address': '7 Cité Paradis, 75010 Paris, France',
                        'lat':  48.8748465,
                        'lng': 2.3504873
                        }
        geosearch_response = [3504931, 5475546, 5653202, 6035646]
        wiki_resp = {'text': ("La cité d'Hauteville est une voie du 10e "
                             "arrondissement de Paris, en France. Situation"
                             " et accès La cité d'Hauteville est une voie"
                             " publique située dans le 10e arrondissement"
                             " de Paris. Elle débute au 82, rue "
                             "d'Hauteville et se termine au 51..."),
                    'title': "Cité d'Hauteville",
                    'url': ("https://fr.wikipedia.org/wiki/"
                            "Cit%C3%A9_d%27Hauteville"),
                    }
        mock_gmap.return_value = gmap_response
        mock_geos.return_value = geosearch_response
        mock_wiki.return_value = wiki_resp


        obj = BuildResponse(self.TEXT[4])
        test_dict = obj.get_response()
        assert test_dict['lat'] == 48.8748465 and test_dict['lng'] == 2.3504873

    def test_special_text_if_not_found_place(self):
        expected_msg = ("Qu'est ce que tu dis ? poudlard ? "
                        "Je ne connais pas ce lieu, ou "
                        "peut-être ai-je mal compris.. veux-tu "
                        "reformuler s'il te plaît ?")

        obj = BuildResponse(self.TEXT[7])
        test_dict = obj.get_response()
        assert test_dict['special_text'] == expected_msg
