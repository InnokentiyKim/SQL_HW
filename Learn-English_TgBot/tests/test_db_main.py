import pytest
from dotenv import load_dotenv
import sys
from database.db_core import engine, Base
from database.db_main import DBManager
from models.bot_user import BotUser
from settings.config import settings
load_dotenv()

class TestDBManager:

    def __init__(self):
        self.db = DBManager(engine=engine)

    def setup_method(self):
        Base.metadata.drop_all(engine)
        self.db = DBManager(engine=engine)


    def teardown_method(self):
        pass


    # @pytest.mark.parametrize(
    #     'user_id, user_name, expected',
    #     [(1, 'John', BotUser), (2, '', BotUser)]
    # )
    # def test_add_new_user(self, user_id, user_name, expected):
    #     result = self.db.add_new_user(user_id, user_name)
    #     assert isinstance(result, expected) == True, f'Expected {expected}, but got {type(result)}'

    # @pytest.mark.parametrize(
    #     'user_id, result',
    #     [(1, 1), (2, None)]
    # )
    # def test_identify_user(self, user_id, expected):
    #     pass


