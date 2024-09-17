from typing import Optional
from models.bot_user import BotUser
from models.word import Word


class PlaySessionCore:
    def __init__(self):
        self.session_id: int = 0
        self.user: Optional[BotUser] = None
        self.target_words: list['Word'] = []
        self.target_word_index: int = 0
        self.current_target_word: Optional['Word'] = None
        self.is_target_list_ended: bool = True
        self.viewed_words: Optional[list[Word]] = []
        self.other_words: Optional[list[Word]] = []

    def refresh_session(self):
        self.target_word_index = 0
        self.is_target_list_ended = False
        self.session_id += 1
