from telebot.apihelper import set_my_commands
from telebot.types import BotCommand
from settings.config import settings, MENU_COMMANDS
from telebot import TeleBot
from handlers.handler_main import HandlerMain
from markup.markups import Markup


class EnglishTelBot:

    __version__ = settings.VERSION
    __author__ = settings.AUTHOR

    def __init__(self):
        self.token = settings.TOKEN
        self.bot = TeleBot(self.token)
        self.handler = HandlerMain(self.bot)
        self.markup = Markup()

    @staticmethod
    def set_bot_menu(commands: dict):
        commands = [BotCommand(command=command, description=description) for command, description in commands.items()]
        set_my_commands(token=settings.TOKEN, commands=commands)

    def start(self):
        self.set_bot_menu(MENU_COMMANDS)
        self.handler.handle()

    def run_bot(self):
        self.start()
        print('English vocabulary bot is running...')
        self.bot.polling(none_stop=True)
