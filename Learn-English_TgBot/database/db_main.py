from database.db_core import Base, Singleton, Session, engine
from database.db_functions import DBFunctions


class DBManager(metaclass=Singleton):
    def __init__(self):
        Base.metadata.create_all(engine)
        self._session = Session()
        self.db_functions = DBFunctions()


