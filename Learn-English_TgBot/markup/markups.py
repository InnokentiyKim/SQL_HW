from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from markup.keyboards import Keyboards


class Markup:

    def __init__(self):
        self.keyboards = Keyboards()
        self.active_keyboard = None

    def _get_words_keyboard(self, buttons_names: list[str]):
        words_buttons = [self.keyboards.set_word_button(button) for button in buttons_names]
        return words_buttons

    def get_menu_keyboard(self, buttons_names: list[str], one_time: bool = False):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
        command_buttons = [self.keyboards.set_command_button(button) for button in buttons_names]
        markup.row(*command_buttons)
        return markup

    def _get_navigation_keyboard(self, buttons_names: list[str]):
        navigation_buttons = [self.keyboards.set_command_button(button) for button in buttons_names]
        return navigation_buttons

    def get_settings_keyboard(self, buttons_names: list[str]):
        settings_buttons = [self.keyboards.set_settings_button(button, data=button) for button in buttons_names]
        markup = InlineKeyboardMarkup(row_width=2)
        markup.row(*settings_buttons)
        return markup

    def get_main_keyboard(self, words: list[str], navigation: list[str], words_in_line: int = 2, commands_in_line: int = 3):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        words_keyboard = self._get_words_keyboard(words)
        navigation_keyboard = self._get_navigation_keyboard(navigation)
        if 0 < words_in_line <= len(words_keyboard):
            for i in range(0, len(words_keyboard), words_in_line):
                markup.row(*words_keyboard[i:i+words_in_line])
        else:
            markup.row(*words_keyboard)
        markup.row()
        if 0 < commands_in_line <= len(navigation_keyboard):
            for i in range(0, len(navigation_keyboard), commands_in_line):
                markup.row(*navigation_keyboard[i:i+commands_in_line])
        else:
            markup.row(*navigation_keyboard)
        return markup

