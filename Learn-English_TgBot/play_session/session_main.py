from random import shuffle, choices
from database.db_main import DBManager
from models.bot_user import BotUser
from models.word import Word
from play_session.session_core import PlaySessionCore
from settings.config import settings, CATEGORIES


class PlaySession(PlaySessionCore):
    def __init__(self):
        super().__init__()
        self.DB = DBManager()

    def init_session(self, bot_user: BotUser, words_category: str = CATEGORIES['COMMON']['name']) -> None:
        self.user = bot_user
        self.target_words = self.DB.get_target_words(self.user.id, category=words_category)
        self.other_words = self.DB.get_other_words(self.user.id, category=words_category)
        if self.target_words:
            shuffle(self.target_words)
            self.refresh_session()

    def _get_next_target_word(self) -> Word | None:
        if self.target_words and not self.is_target_list_ended:
            self.current_target_word = self.target_words[self.target_word_index]
            self.target_word_index += 1
            return self.current_target_word
        else:
            self.is_target_list_ended = True
            return None

    def _get_next_other_words(self, amount: int) -> list[Word]:
        if self.other_words and len(self.other_words) >= amount:
            return choices(population=self.other_words, k=amount)
        else:
            return []

    def get_words_for_card(self, other_words_amount: int = settings.WORDS_IN_CARDS - 1) -> dict[str, list[Word] | Word] | None:
        target_word = self._get_next_target_word()
        other_words = self._get_next_other_words(other_words_amount)
        all_words = [target_word] + other_words
        if not target_word or not other_words:
            return None
        return {'target': target_word, 'other': other_words, 'all': all_words}





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
