from app.Grandpy.parser import Parser


class TestParser:

    TEXT = ["Hello",
            "Comment vas-tu ?",
            "Bonsoir, tu vas bien ?",
            "Salut, tu sais où est l'arc de triomphe ?",
            "Coucou, tu vas bien ? tu sais où est l'arc de triomphe au fait ?",
            "Où est le Groenland ?",
            "Salut, tu vas bien ? où est Groenland exactement ?",
            "Tu sais où se trouve poudlard ?",
            "Salut, tu saurais où est poudlard par hasard ?",
            "Salut GrandPy ! Est-ce que tu connais l'adresse"
            " d'OpenClassrooms ?",
            "Bonsoir Grandpy, j'espère que tu as passé une belle semaine."
            " Est-ce que tu pourrais m'indiquer l'adresse de la tour eiffel ?"
            " Merci d'avance et salutations à mamie",
            "Salut Grandpy ! Comment s'est passé ta soirée avec Grandma Hier"
            " soir ? Au fait, pendant que j'y pense, pourrais-tu m'indiquer"
            " où se trouve le musée d'art et d'histoire de Fribourd,"
            " s'il te plaît ?",
            "Bonsoir Grandpy ! Comment vas-tu ? Dis moi, sais-tu où se trouve "
            "le Lac de vassivière précisément ?",
            "Je voudrais aller à la tour eiffel"]

    KEYWORDS = ["",
                "",
                "",
                "l'arc triomphe",
                "l'arc triomphe",
                "groenland",
                "groenland",
                "poudlard",
                "poudlard",
                "openclassrooms",
                "la tour eiffel",
                "musee d'art d'histoire fribourd",
                "lac vassiviere",
                "la tour eiffel"]

    SPECIAL_TEXT = ["Hello la jeunesse ! ",
                    "Et bien ma foi, je suis en pleine forme aujourd'hui ! ",
                    "Bonsoir la jeunesse ! Et bien ma foi, je suis en pleine "
                    "forme aujourd'hui ! ",
                    "Salut la jeunesse ! ",
                    "Coucou la jeunesse ! Et bien ma foi, je suis en pleine "
                    "forme aujourd'hui ! ",
                    "Salut la jeunesse ! Et bien ma foi, je suis en pleine "
                    "forme aujourd'hui ! ",
                    "Salut la jeunesse ! Et bien ma foi, je suis en pleine "
                    "forme aujourd'hui ! ",
                    "Salut la jeunesse ! ",
                    "Salut la jeunesse ! ",
                    "Salut la jeunesse ! ",
                    "Bonsoir la jeunesse ! ",
                    "Salut la jeunesse ! ",
                    "Bonsoir la jeunesse ! Et bien ma foi, je suis en pleine "
                    "forme aujourd'hui ! "
                    ]

    def test_parse(self):
        for i, j in enumerate(self.TEXT):
            obj = Parser(j)
            response = obj.parse()
            assert response['keyword'] == self.KEYWORDS[i]

    def test_special_text(self):
        for i, j in enumerate(self.TEXT):
            obj = Parser(j)
            response = obj.parse()
            if 'special_text' in response.keys():
                assert response['special_text'] == self.SPECIAL_TEXT[i]
