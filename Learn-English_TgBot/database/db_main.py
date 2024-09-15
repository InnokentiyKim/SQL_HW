from database.db_core import Base, Singleton, Session, engine
from database.db_functions import DBFunctions


class DBManager(metaclass=Singleton):
    def __init__(self):
        Base.metadata.create_all(engine)
        self._session = Session()
        self.db_functions = DBFunctions()

    def start_actions(self, user_id: int, user_name: str):
        if not self.db_functions.identify_user(user_id):
            self.db_functions.add_new_user(user_id, user_name)
