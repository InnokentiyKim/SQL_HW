from models.word import Word


class UserSession:
    def __init__(self):
        self.words_list = None
        self.target_word = None
        self.target_eng = None
        self.target_rus = None
        self.used_words = []

    def _set_target(self, word):
        self.target_word = word
        self.target_eng = word.eng_title
        self.target_rus = word.rus_title
        self.used_words.append(word)

    def _set_words_list(self, words):
        self.words_list = words

    def initialize_user_words(self, words):
        if words and isinstance(words, Word):
            self._set_words_list(words)
            self._set_target(words[0])

