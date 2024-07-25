from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from settings import config
from data_base.dbalchemy import DBManager
from models.word import Word


class TargetWords:
    def __init__(self):
        self.target_word = None
        self.target_eng = None
        self.target_rus = None

    def set_target(self, word):
        if isinstance(word, Word):
            self.target_word = word
            self.target_eng = word.eng_title
            self.target_rus = word.rus_title


class Keyboards:

    def __init__(self):
        self.markup = None
        self.DB = DBManager()
        self.target_word = TargetWords()

    def set_command_button(self, name):
        return KeyboardButton(config.KEYBOARD['name'])

    def set_word_button(self, name):
        return KeyboardButton(name)

    def cards_desk(self, user_id):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        words = self.DB.get_next_card(user_id)
        self.target_word.set_target(words[0])
        item_buttons = [self.set_word_button(word.eng_title) for word in words]
        self.markup.row(item_buttons[0], item_buttons[1])
        self.markup.row(item_buttons[2], item_buttons[3])
        return self.markup
