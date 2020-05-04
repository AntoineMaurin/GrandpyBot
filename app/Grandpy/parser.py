from . import words
import unicodedata

"""This class is made to find out what the user asked in the form, and
return results into a usable format, which is actually a dictionnary."""


class Parser:

    def __init__(self, text):
        self.text = text
        self.response = {}

    """The main method, calls one by one the methods of this class to parse
    the text step by step. Then returns the result dictionnary."""
    def parse(self):
        pure_text = self.delete_accents_and_lower(self.text)
        self.response['initial_text'] = pure_text

        text_without_special_words = self.look_for_special_text(pure_text)
        reduced_part = self.search_keyword_part(text_without_special_words)
        keyword = self.remove_remaining_words(reduced_part)

        self.response['keyword'] = keyword

        if self.response['special_text'] == '':
            del self.response['special_text']

        return self.response

    """This method just deletes accents and lower the text, before returning
    it clean."""
    def delete_accents_and_lower(self, text):
        cl_text = unicodedata.normalize("NFKD", text).encode('ascii', "ignore")
        text = cl_text.lower().decode()

        for w in text:
            if w in words.punctuation:
                text = text.replace(w, '')
        return text

    """This one looks for hello or how are you parts in the text, and puts it
    under the 'special_text' key."""
    def look_for_special_text(self, text):
        how_are_you = ''
        for word in words.how_are_you:
            if word in text:
                how_are_you = ("Et bien ma foi, je suis en pleine forme "
                               "aujourd'hui ! ")
                text = text.replace(word, '')

        hello = ''
        for word in words.hello_words:
            if word in text:
                hello = (word.capitalize() + " la jeunesse ! ")
                text = text.replace(word, '')

        total_special_text = hello + how_are_you
        self.response['special_text'] = total_special_text
        return text

    """This method reduces the area around the keyword by checking if there is
    a pre-keyword formula in the text. If yes, it keeps the part from this
    sentence part to the next '?'."""
    def search_keyword_part(self, text):
        start_pos = 0
        for word in words.pre_keyword_words:
            if word in text:
                start_pos = text.find(word) + len(word)

        end_pos = len(text)
        end_pos_list = [pos for pos, char in enumerate(text) if char == '?']

        for id, value in enumerate(end_pos_list):
            if start_pos < value:
                end_pos = end_pos_list[id]

        reduced_zone = text[start_pos:end_pos]
        return reduced_zone

    """Thid method tries to remove what's left, by erasing words if they are in
    the lists politeness_words or stopwords in the file words.py."""
    def remove_remaining_words(self, text):
        words.stopwords.extend(words.politeness_words)
        text_list = text.split()
        for word in words.stopwords:
            if word in text_list:
                text = text.replace(word, '')
        text = text.split()

        return " ".join(text)
