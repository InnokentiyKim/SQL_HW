from telebot.types import KeyboardButton
from settings import config


class Keyboards:

    @staticmethod
    def set_command_button(name: str):
        return KeyboardButton(config.KEYBOARD[name])

    @staticmethod
    def set_word_button(name: str):
        return KeyboardButton(name)
