from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:

    def __init__(self):
        self.markup = None
        self.DB = DBManager()

    def set_command_button(self, name):
        return KeyboardButton(config.KEYBOARD['name'])

    def set_word_button(self, name):
        return KeyboardButton(name)

    def cards_desk(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        words = ['самолет', 'вертолет', 'автомобиль', 'веревка']
        item_buttons = [self.set_word_button(button) for button in words]
        self.markup.row(item_buttons[0], item_buttons[1])
        self.markup.row(item_buttons[2], item_buttons[3])
        return self.markup
