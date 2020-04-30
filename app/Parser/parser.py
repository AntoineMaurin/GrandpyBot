from . import words
import unicodedata

class Parser:

    def __init__(self, text):
        self.text = text

    def parse(self):
        pure_text = self.delete_accents_and_lower(self.text)
        reduced_part = self.search_keyword_part(pure_text)
        keyword = self.remove_remaining_words(reduced_part)

        return keyword

    def delete_accents_and_lower(self, text):
        clean_text = unicodedata.normalize("NFKD", text).encode('ascii', "ignore")
        text = clean_text.lower().decode()

        for w in text:
            if w in words.punctuation:
                text = text.replace(w, '')
        return text

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

    def remove_remaining_words(self, text):
        words.stopwords.extend(words.politeness_words)
        text_list = text.split()
        for word in words.stopwords:
            if word in text_list:
                text = text.replace(word, '')
        text = text.split()

        return " ".join(text)
