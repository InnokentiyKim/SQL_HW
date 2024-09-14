from random import choices
from typing import Any
from session_data import UsersPlaySession
from settings.config import settings
from source.data_models import TargetWord


class PlaySession(UsersPlaySession):
    def __init__(self):
        super().__init__()

    def get_other_words_for_card(self, amount: int = settings.WORDS_IN_CARDS - 1) -> list[Any]:
        if self.other_words and len(self.other_words) >= amount:
            return choices(population=self.other_words, k=amount)
        else:
            return []

    def get_next_target_word(self) -> TargetWord | None:
        if self.target_words and self.target_word_index < len(self.target_words):
            target_word = self.target_words[self.target_word_index]
            self.target_word_index += 1
            return target_word
        else:
            self.is_target_list_ended = True
            return None

