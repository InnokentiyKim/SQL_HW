from telebot.types import KeyboardButton, InlineKeyboardButton
from settings import config


class Keyboards:

    @staticmethod
    def set_command_button(name: str):
        return KeyboardButton(name)

    @staticmethod
    def set_word_button(name: str):
        return KeyboardButton(name)

    @staticmethod
    def set_settings_button(name: str, data: str):
        return InlineKeyboardButton(name, callback_data=data)
