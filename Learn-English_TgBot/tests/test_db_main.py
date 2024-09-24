import pytest
from dotenv import load_dotenv
from database.db_core import engine, Base
from database.db_main import DBManager
load_dotenv()

class TestDBManager:

    def __init__(self):
        self.db = DBManager(engine=engine)

    def setup_method(self):
        Base.metadata.drop_all(engine)
        self.db = DBManager(engine=engine)


    def teardown_method(self):
        Base.metadata.drop_all(engine)


