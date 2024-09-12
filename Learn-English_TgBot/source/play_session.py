from random import choices
from typing import Optional, Any
from models.bot_user import BotUser
from settings.config import settings
from source.data_models import TargetWord


class UsersPlaySession:
    def __init__(self):
        self.session_id: Optional[int] = None
        self.user: Optional[BotUser] = None
        self.target_words: Optional[list[TargetWord]] = None
        self.target_word_index: int = 0
        self.viewed_words: Optional[list[TargetWord]] = None
        self.other_words: Optional[list[str]] = None

    def get_other_words_for_card(self, amount: int = settings.WORDS_IN_CARDS - 1) -> list[Any]:
        if self.other_words and len(self.other_words) >= amount:
            return choices(population=self.other_words, k=amount)
        else:
            return []

    def get_next_target_word(self) -> TargetWord | None:
        if self.target_word_index < len(self.target_words):
            target_word = self.target_words[self.target_word_index]
            self.target_word_index += 1
            return target_word
        else:
            return None
