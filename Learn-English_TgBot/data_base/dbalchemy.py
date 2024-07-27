from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_base.db_core import Base
from settings import config
from functools import wraps
from models.category import Category
from models.user import User
from models.word import Word
from models.category_word import CategoryWord
import json
import sqlalchemy as sa


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    def __init__(self):
        self.engine = create_engine(config.DSN)
        Session = sessionmaker(bind=self.engine)
        self._session = Session()
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.init_default_cards()
        self.user_words = None
        self.target_word = None
        self.viewed_words = []

    # def use_active_session(self):
    #     def decor(func):
    #         @wraps(func)
    #         def wrapper(*args, **kwargs):
    #             with self._session as sess:
    #                 result = func(*args, **kwargs)
    #             return result
    #         return wrapper
    #     return decor

    def identify_user(self, user_id):
        with self._session as session:
            familiar = session.query(User.id).filter(User.id == user_id).all()
            return True if familiar else False

    def get_random_cards(self, user_id, amount=4):
        with self._session as session:
            random_words = session.query(Word).join(User, Word.user_id == User.id).filter(User.id == user_id).order_by(sa.func.random()).limit(amount).all()
            return random_words

    def get_next_card(self, user_id) -> None:
        self.user_words = self.get_random_cards(user_id)
        self.target_word = self.user_words[0]
        self.viewed_words.append(self.target_word)

    def close(self):
        self._session.close()

    def init_default_cards(self):
        with open('data_base/default_words.json') as file:
            default_words = json.load(file)
        models = {'user': User, 'word': Word, 'category': Category}
        for line in default_words:
            model = models[line.get('model')]
            self._session.add(model(id=line.get('pk'), **line.get('fields')))
        self._session.commit()
        category_word_examples = [
        {"category_id": 1, "word_id": 1},
        {"category_id": 1, "word_id": 2},
        {"category_id": 1, "word_id": 3},
        {"category_id": 1, "word_id": 4},
        {"category_id": 1, "word_id": 5},
        {"category_id": 1, "word_id": 6},
        {"category_id": 1, "word_id": 7},
        {"category_id": 1, "word_id": 8},
        {"category_id": 1, "word_id": 9},
        {"category_id": 1, "word_id": 10}
        ]
        for example in category_word_examples:
            self._session.add(CategoryWord(**example))
        self._session.commit()
        self.close()

