from telebot.types import BotCommand, BotCommandScopeDefault, MenuButton, MenuButtonCommands, BotCommandScopeChat
from settings.config import settings, MENU_COMMANDS, COMMANDS
from telebot import TeleBot
from handlers.handler_main import HandlerMain


class EnglishTelBot:

    __version__ = settings.VERSION
    __author__ = settings.AUTHOR

    def __init__(self):
        self.token = settings.TOKEN
        self.bot = TeleBot(self.token, parse_mode='html')
        self.handler = HandlerMain(self.bot)

    def set_bot_menu(self, commands: dict):
        menu_commands = [BotCommand(key, value) for key, value in commands.items()]
        self.bot.set_my_commands(menu_commands)


    def start(self):
        self.set_bot_menu(MENU_COMMANDS)
        self.handler.handle()

    def run_bot(self):
        self.start()
        print('English vocabulary bot is running...')
        self.bot.polling(none_stop=True)
