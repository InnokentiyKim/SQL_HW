from time import sleep
from telebot.types import BotCommand, BotCommandScopeDefault, MenuButton, MenuButtonCommands, BotCommandScopeChat
from bot_logging.bot_logging import error_logger
from settings.config import settings, MENU_COMMANDS, COMMANDS
from telebot import TeleBot
from handlers.handler_main import HandlerMain


class EnglishTelBot:
    """
    Класс для работы с ботом
    Атрибуты:
        __version__ - версия бота
        __author__ - автор бота
        token - токен бота
        bot - объект бота
        handler - обработчик
    Методы:
        set_bot_menu(commands) - устанавливает меню бота
        start() - запускает бота
    """

    __version__ = settings.VERSION
    __author__ = settings.AUTHOR

    def __init__(self):
        self.token = settings.TOKEN
        self.bot = TeleBot(self.token, parse_mode='html')
        self.handler = HandlerMain(self.bot)

    def set_bot_menu(self, commands: dict):
        """
        Устанавливает меню бота
        Параметры:
            commands (dict): Словарь команд бота
        """
        menu_commands = [BotCommand(key, value) for key, value in commands.items()]
        self.bot.set_my_commands(menu_commands)


    def start(self):
        """
        Запускает бота
        """
        self.set_bot_menu(MENU_COMMANDS)
        self.handler.handle()

    def run_bot(self):
        try:
            self.start()
            print('English vocabulary bot is running...')
            self.bot.polling(none_stop=True)
        except Exception as error:
            error_logger.error(error, exc_info=True)
            print('Something went wrong...Restarting...')
            sleep(settings.DELAY_SEC)
            self.run_bot()
