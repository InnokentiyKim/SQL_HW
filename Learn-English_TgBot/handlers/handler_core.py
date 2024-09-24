import abc
from database.db_core import engine
from markup.markups import Markup
from database.db_main import DBManager


class Handler(metaclass=abc.ABCMeta):
    """
    Абстрактный класс обработчика.
    Описывает общие методы обработчиков.
    Атрибуты:
        bot: Объект бота.
        markup: Объект маркировки (клавиатуры).
        DB: Объект менеджера базы данных.
    """

    def __init__(self, bot):
        self.bot = bot
        self.markup = Markup()
        self.DB = DBManager(engine=engine)

    @abc.abstractmethod
    def handle(self):
        pass
