from random import shuffle

from requests.packages import target

from database.db_main import DBManager
from markup.markups import Markup
from models.bot_user import BotUser
from play_session.session_core import PlaySessionCore
from settings.config import settings, CATEGORIES
from source.data_models import TargetWord, OtherWord


class PlaySession(PlaySessionCore):
    def __init__(self):
        super().__init__()
        self.DB = DBManager()
        self.markup = Markup()

    def init_session(self, bot_user: BotUser, category: str = CATEGORIES['COMMON']['name']) -> None:
        self.session_id = 0
        self.user = bot_user
        self.target_words = self.DB.get_target_words(self.user.id, category=category)
        self.other_words = self.DB.get_other_words(self.user.id, category=category)
        if self.target_words:
            shuffle(self.target_words)
            self.target_word_index = 0
            self.is_target_list_ended = False

    def _get_next_target_word(self) -> TargetWord | None:
        return self.target_words[self.target_word_index] if not self.is_target_list_ended else None

    def get_next_play_card(self, ):
        target_word =






        self.session_id: Optional[int] = 0
        self.user: Optional[BotUser] = None
        self.target_words: list[TargetWord] = []
        self.target_word_index: int = 0
        self.is_target_list_ended: bool = True
        self.viewed_words: Optional[list[TargetWord]] = []
        self.other_words: Optional[list[OtherWord]] = []

    def get_other_words(self, amount: int = settings.WORDS_IN_CARDS - 1) -> list[OtherWord]:
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

    def start_session(self, user_id: int):
        self.user = self.DB.get_user(user_id)

    def form_words_card(self):
        target_word = self._get_next_target_word()
        other_words = self._get_other_words()
        return {'target_word': target_word, 'other_words': other_words}

    def form_words_desk(self, words: list[str], items_in_line: int = 2):
        pass

    # def _cards_desk(self, words: list[str], items_in_line: int = 2):
    #     self.markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    #     self.DB.get_next_card(user_id)
    #     words = self.DB.user_words
    #     if play_mode == 0:
    #         item_buttons = [[self.set_word_button(word.eng_title)] for word in words]
    #     for count, item in enumerate(item_buttons):
    #         self.markup.row(item)
    #     self.markup.row(item_buttons[0], item_buttons[1])
    #     self.markup.row()
    #     self.markup.row(item_buttons[2], item_buttons[3])
    #     return self.markup

    # def get_next_word_keyboard(self, user_id: int):
    #     self.DB.is_answered = False
    #     self.markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    #     self.markup = self._cards_desk(user_id)
    #     menu_button = self.keyboards.set_command_button('MENU')
    #     next_step_button = self.keyboards.set_command_button('NEXT_STEP')
    #     self.markup.row(menu_button, next_step_button)
    #     self.active_keyboard = self.markup
    #     return self.markup

    # def get_menu_keyboard(self):
    #     buttons = ['ADD_WORD', 'DELETE_WORD', 'SETTINGS', 'BACK', 'INFO']
    #     return self.get_menu_markup(buttons)
