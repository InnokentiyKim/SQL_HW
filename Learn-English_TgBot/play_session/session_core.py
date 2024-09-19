from typing import Optional
from models.bot_user import BotUser
from models.word import Word
from settings.config import settings


class PlaySessionCore:
    def __init__(self):
        self.session_id: int = 0
        self.user: Optional[BotUser] = None
        self.target_words: list['Word'] = []
        self.target_word_index: int = 0
        self.current_target_word: Optional['Word'] = None
        self.attempts_count: int = 0
        self.is_answered: bool = False
        self.is_target_list_ended: bool = True
        self.viewed_words: Optional[list[Word]] = []
        self.other_words: Optional[list[Word]] = []

    def refresh_current_word_stats(self):
        self.is_answered = False
        self.attempts_count = 0

    def refresh_session(self):
        self.target_word_index = 0
        self.is_target_list_ended = False
        self.session_id += 1

    def increase_target_words_stats(self) -> None:
        self.is_answered = True
        self.current_target_word.word_stats.number_of_attempts += 1
        self.current_target_word.word_stats.successful_attempts += 1
        self.current_target_word.word_stats.success_streak += 1
        if self.current_target_word.word_stats.success_streak >= settings.IS_STUDIED_COND:
            self.current_target_word.word_stats.is_studied = 1

    def decrease_target_words_stats(self) -> None:
        self.current_target_word.word_stats.number_of_attempts += 1
        self.current_target_word.word_stats.success_streak = 0

    def increase_player_stats(self) -> None:
        self.user.user_stats.number_of_attempts += 1
        self.user.user_stats.successful_attempts += 1
        self.user.user_stats.success_streak += 1

    def decrease_player_stats(self) -> None:
        self.user.user_stats.number_of_attempts += 1
        self.user.user_stats.success_streak = 0
