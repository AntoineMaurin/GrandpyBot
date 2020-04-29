from app.Parser.parser import Parser
from unittest.mock import Mock, patch

import pytest

class TestParser:

    TEXT = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"

    # def test_parser_text(self):
    #     obj = Parser(self.TEXT)
    #     r = obj.parse()
    #     assert r == 'OpenClassrooms'
