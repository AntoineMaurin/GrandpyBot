from words import stopwords

class Parser:

    def __init__(self, text):
        self.text = text

    def remove_stop_words(self, text):
        final_string = ""

        list_text = (text.split())

        [list_text.remove(elt) for elt in list_text if elt in stopwords]

        print(list_text)

        final_string = " ".join(list_text)
        return final_string

    def parse(self):
        text_to_parse = self.remove_stop_words(self.text)

        return text_to_parse

# test = Parser("Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?")
# print("initial text : ", test.text, "\n")
# print("\ntext without stopwords : ", test.parse())
