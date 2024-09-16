from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from markup.keyboards import Keyboards


class Markup:

    def __init__(self):
        self.keyboards = Keyboards()
        self.active_keyboard = None

    @staticmethod
    def get_markup(buttons: list, items_in_line: int = 1, one_time: bool = False):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
        if 0 < items_in_line <= len(buttons):
            for i in range(0, len(buttons), items_in_line):
                markup.row(*buttons[i:i+items_in_line])
                markup.row()
        else:
            markup.row(*buttons)
        return markup

    def get_words_markup(self, buttons_names: list[str], items_in_line: int = 2, one_time: bool = False):
        words_buttons = [self.keyboards.set_word_button(button) for button in buttons_names]
        markup = self.get_markup(words_buttons, items_in_line=items_in_line, one_time=one_time)
        return markup

    def get_menu_markup(self, buttons_names: list[str], items_in_line: int = 2, one_time=False):
        command_buttons = [self.keyboards.set_command_button(button) for button in buttons_names]
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
        self.get_markup(command_buttons, items_in_line=items_in_line, one_time=one_time)
        return markup

    def get_navigation_markup(self, buttons_names: list[str], items_in_line: int = 1):
        navigation_buttons = [self.keyboards.set_command_button(button) for button in buttons_names]
        markup = self.get_markup(navigation_buttons, items_in_line=items_in_line)
        return markup

    def get_next_word_keyboard(self, user_id: int):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        self.markup = self._cards_desk(user_id)
        menu_button = self.keyboards.set_command_button('MENU')
        next_step_button = self.keyboards.set_command_button('NEXT_STEP')
        self.markup.row(menu_button, next_step_button)
        self.active_keyboard = self.markup
        return self.markup

