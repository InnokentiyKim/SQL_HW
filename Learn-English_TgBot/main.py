import telebot
from settings import config
from telebot import types, TeleBot
from handlers.handler_main import HandlerMain
from random import shuffle

TOKEN = '7248775992:AAGVlmeqr1XgnoaCi8XrQEIBL14bjsOQL_Q'

class TelBot:

    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        self.token = config.TOKEN
        self.bot = TeleBot(self.token)
        self.handler = HandlerMain(self.bot)

    def start(self):
        self.handler.handle()

    def run_bot(self):
        self.start()
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    bot = TelBot()
    bot.run_bot()
