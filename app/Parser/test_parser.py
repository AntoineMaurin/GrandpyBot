from app.Parser.parser import Parser
from unittest.mock import Mock, patch

import pytest

class TestParser:

    TEXT = ["Salut GrandPy ! Est-ce que tu connais l'adresse"
            " d'OpenClassrooms ?",
            "Bonsoir Grandpy, j'espère que tu as passé une belle semaine."
            " Est-ce que tu pourrais m'indiquer l'adresse de la tour eiffel ?"
            " Merci d'avance et salutations à mamie",
            "Salut Grandpy ! Comment s'est passé ta soirée avec Grandma Hier"
            " soir ? Au fait, pendant que j'y pense, pourrais-tu m'indiquer"
            " où se trouve le musée d'art et d'histoire de Fribourd,"
            " s'il te plaît ?",
            "Où trouve-t-on le Lac de vassivière au juste ?"]

    RESPONSES = ["openclassrooms",
                 "tour eiffel",
                 "musee d'art d'histoire fribourd",
                 "lac vassiviere"]

    def test_parser_text(self):
        for i, j in enumerate(self.TEXT):
            obj = Parser(j)
            r = obj.parse()
            assert r['keyword'] == self.RESPONSES[i]

    def test_return_type(self):
        obj = Parser(self.TEXT[0])
        r = obj.parse()
        assert isinstance(r, dict)

    def test_delete_accents_and_lower(self):
        obj = Parser(self.TEXT[2])
        r = obj.delete_accents_and_lower(self.TEXT[2])
        assert r == ("salut grandpy  comment s'est passe ta soiree avec"
                     " grandma hier soir ? au fait pendant que j'y pense"
                     " pourrais-tu m'indiquer ou se trouve le musee d'art"
                     " et d'histoire de fribourd s'il te plait ?")

    def test_search_keyword_part(self):
        obj = Parser(self.TEXT[2])
        test_pure_text = obj.delete_accents_and_lower(self.TEXT[2])
        r = obj.search_keyword_part(test_pure_text)
        assert r == " le musee d'art et d'histoire de fribourd s'il te plait "

    def test_remove_remaining_words(self):
        obj = Parser(self.TEXT[2])
        test_pure_text = obj.delete_accents_and_lower(self.TEXT[2])
        reduced_part = obj.search_keyword_part(test_pure_text)
        r = obj.remove_remaining_words(reduced_part)
        assert r == "musee d'art d'histoire fribourd"
