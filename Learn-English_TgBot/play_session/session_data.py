from typing import Optional
from models.bot_user import BotUser
from source.data_models import TargetWord


class UsersPlaySession:
    def __init__(self):
        self.session_id: Optional[int] = None
        self.user: Optional[BotUser] = None
        self.target_words: list[TargetWord] = []
        self.target_word_index: int = 0
        self.is_target_list_ended: bool = True
        self.viewed_words: Optional[list[TargetWord]] = None
        self.other_words: Optional[list[str]] = None

    def refresh_session(self):
        self.target_word_index = 0
        self.is_target_list_ended = False
