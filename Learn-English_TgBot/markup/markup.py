from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:

    def __init__(self):
        self.markup = None
        self.DB = DBManager()
        self.active_keyboard = None

    @staticmethod
    def set_command_button(name: str):
        return KeyboardButton(config.KEYBOARD[name])

    @staticmethod
    def set_word_button(name: str):
        return KeyboardButton(name)

    def _cards_desk(self, user_id):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        self.DB.get_next_card(user_id)
        words = self.DB.user_words
        item_buttons = [self.set_word_button(word.eng_title) for word in words]
        self.markup.row(item_buttons[0], item_buttons[1])
        self.markup.row(item_buttons[2], item_buttons[3])
        return self.markup

    def get_next_word_keyboard(self, user_id: int):
        self.DB.is_answered = False
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        self.markup = self._cards_desk(user_id)
        menu_button = self.set_command_button('MENU')
        next_step_button = self.set_command_button('NEXT_STEP')
        self.markup.row(menu_button, next_step_button)
        self.active_keyboard = self.markup
        return self.markup

    def get_menu_keyboard(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        add_word_button = self.set_command_button('ADD_WORD')
        delete_word_button = self.set_command_button('DELETE_WORD')
        settings_button = self.set_command_button('SETTINGS')
        back_button = self.set_command_button('BACK')
        info_button = self.set_command_button('INFO')
        self.markup.row(add_word_button, delete_word_button)
        self.markup.row(back_button, settings_button, info_button)
        return self.markup
