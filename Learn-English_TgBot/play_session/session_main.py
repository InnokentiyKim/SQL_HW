from random import shuffle
import requests

from database.db_core import engine
from database.db_main import DBManager
from models.bot_user import BotUser
from models.word import Word
from play_session.session_core import PlaySessionCore
from settings.config import settings, CATEGORIES


class PlaySession(PlaySessionCore):
    def __init__(self):
        super().__init__()
        self.DB = DBManager(engine=engine)

    def init_session(self, bot_user: BotUser, words_category: str, words_amount: int) -> None:
        self.user = bot_user
        self.target_words = self.DB.get_target_words(self.user.id, category=words_category, amount=words_amount)
        self.other_words = self.DB.get_other_words(self.user.id, category=words_category)
        if self.target_words:
            self.refresh_session()

    def _get_next_target_word(self) -> Word | None:
        if self.target_words and not self.is_target_list_ended:
            self.current_target_word = self.target_words[self.target_word_index]
            self.refresh_current_word_stats()
            self.target_word_index += 1
            if self.target_word_index >= len(self.target_words):
                self.is_target_list_ended = True
            return self.current_target_word
        return None

    def _get_next_other_words(self, target: Word, amount: int) -> list[Word]:
        if target and self.other_words:
            if len(self.other_words) <= amount:
                return []
            choices_list = list(self.other_words)
            for i, word in enumerate(choices_list):
                if word.id == target.id:
                    choices_list.pop(i)
            shuffle(choices_list)
            return choices_list[:amount]
        return []

    def get_words_for_card(self, other_words_amount: int = settings.WORDS_IN_CARDS - 1) -> dict[str, list[Word] | Word] | None:
        target_word = self._get_next_target_word()
        other_words = self._get_next_other_words(target_word, other_words_amount)
        all_words = [target_word] + other_words
        if target_word and other_words:
            return {'target': target_word, 'other': other_words, 'all': all_words}
        return None

    @staticmethod
    def get_words_description(word: str) -> str:
        # TODO: Add caching
        cached = {}
        if word in cached:
            return cached[word]
        try:
            words_api_url = f"{settings.WORDS_URL}{word}"
            response = requests.get(words_api_url).json()
            description = response[0].get('meanings')[0].get('definitions')[0].get('definition')
            cached[word] = description
        except Exception as error:
            description = None
        return description
