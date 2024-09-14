from random import choices
from play_session.session_core import PlaySessionCore
from settings.config import settings
from source.data_models import TargetWord, OtherWord


class PlaySession(PlaySessionCore):
    def __init__(self):
        super().__init__()

    def _get_other_words(self, amount: int = settings.WORDS_IN_CARDS - 1) -> list[OtherWord]:
        if self.other_words and len(self.other_words) >= amount:
            return choices(population=self.other_words, k=amount)
        else:
            return []

    def _get_next_target_word(self) -> TargetWord | None:
        if self.target_words and self.target_word_index < len(self.target_words):
            target_word = self.target_words[self.target_word_index]
            self.target_word_index += 1
            return target_word
        else:
            self.is_target_list_ended = True
            return None

    def form_words_card(self):
        target_word = self._get_next_target_word()
        other_words = self._get_other_words()
        return target_word, other_words
