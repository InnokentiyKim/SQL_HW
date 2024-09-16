import abc
from markup.markups import Keyboards, Markup
from database.db_main import DBManager


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, bot):
        self.bot = bot
        self.markup = Markup()
        self.DB = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass