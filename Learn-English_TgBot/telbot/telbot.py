from settings.config import settings
from telebot import TeleBot
from handlers.handler_main import HandlerMain


class EnglishTelBot:

    __version__ = settings.VERSION
    __author__ = settings.AUTHOR

    def __init__(self):
        self.token = settings.TOKEN
        self.bot = TeleBot(self.token)
        self.handler = HandlerMain(self.bot)

    def start(self):
        self.handler.handle()

    def run_bot(self):
        self.start()
        print('English vocabulary bot is running...')
        self.bot.polling(none_stop=True)
