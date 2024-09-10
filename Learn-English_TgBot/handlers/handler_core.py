import abc
from markup.markup import Keyboards
from database.db_main import DBManager


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, bot):
        self.bot = bot
        self.keyboards = Keyboards()
        self.DB = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass