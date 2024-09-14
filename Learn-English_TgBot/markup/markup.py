from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from markup.keyboards import Keyboards
from database.db_main import DBManager


class Markup:

    def __init__(self):
        self.markup = None
        self.DB = DBManager()
        self.keyboards = Keyboards()
        self.active_keyboard = None

    def _cards_desk(self, user_id, play_mode=0, items_in_line=2):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        self.DB.get_next_card(user_id)
        words = self.DB.user_words
        if play_mode == 0:
            item_buttons = [[self.set_word_button(word.eng_title)] for word in words]
        for count, item in enumerate(item_buttons):
            self.markup.row(item)
        self.markup.row(item_buttons[0], item_buttons[1])
        self.markup.row()
        self.markup.row(item_buttons[2], item_buttons[3])
        return self.markup

    def get_next_word_keyboard(self, user_id: int):
        self.DB.is_answered = False
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        self.markup = self._cards_desk(user_id)
        menu_button = self.keyboards.set_command_button('MENU')
        next_step_button = self.keyboards.set_command_button('NEXT_STEP')
        self.markup.row(menu_button, next_step_button)
        self.active_keyboard = self.markup
        return self.markup

    def get_menu_keyboard(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        add_word_button = self.keyboards.set_command_button('ADD_WORD')
        delete_word_button = self.keyboards.set_command_button('DELETE_WORD')
        settings_button = self.keyboards.set_command_button('SETTINGS')
        back_button = self.keyboards.set_command_button('BACK')
        info_button = self.keyboards.set_command_button('INFO')
        self.markup.row(add_word_button, delete_word_button)
        self.markup.row(back_button, settings_button, info_button)
        return self.markup
