from random import choices
from typing import Optional, Any
from pydantic import BaseModel, PositiveInt
from models.bot_user import BotUser
from settings.config import settings
from source.data_models import TargetWord


class UsersPlaySession(BaseModel):
    session_id: Optional[PositiveInt]
    user: Optional[BotUser]
    target_words: Optional[list[TargetWord]] = None
    target_word_index: int = 0
    viewed_words: Optional[list[TargetWord]] = None
    other_words: Optional[list[str]] = None

    def get_other_words_for_card(self, amount: int = settings.WORDS_IN_CARDS - 1) -> list[Any]:
        if self.other_words and len(self.other_words) >= amount:
            return choices(population=self.other_words, k=amount)
        else:
            return []

    target_words_generator = (word for word in target_words)

    def get_next_target_word(self) -> TargetWord | None:
        if self.target_word_index < len(self.target_words):
            target_word = self.target_words[self.target_word_index]
            self.target_word_index += 1
            return target_word
        else:
            return None
        