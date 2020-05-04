from app.Grandpy.parser import Parser


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
            "Salut Grandpy ! Comment vas-tu ? Dis moi, sais-tu où se trouve le"
            " Lac de vassivière précisément ?"]

    RESPONSES = ["openclassrooms",
                 "la tour eiffel",
                 "musee d'art d'histoire fribourd",
                 "lac vassiviere"]

    def test_parse(self):
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

    def test_look_for_special_text(self):
        obj = Parser(self.TEXT[3])
        test_text = obj.delete_accents_and_lower(self.TEXT[3])
        obj.look_for_special_text(test_text)
        assert obj.response['special_text'] == ("Salut la jeunesse ! Et bien "
                                                "ma foi, je suis en pleine "
                                                "forme aujourd'hui ! ")

    def test_special_text_gets_removed(self):
        obj = Parser(self.TEXT[3])
        test_text = obj.delete_accents_and_lower(self.TEXT[3])
        test_result = obj.look_for_special_text(test_text)
        assert test_result == (" grandpy   ? dis moi sais-tu ou se trouve "
                               "le lac de vassiviere precisement ?")

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
