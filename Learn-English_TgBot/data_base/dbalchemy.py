from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_base.db_core import Base
from settings.config import DSN, CATEGORY
from models.category import Category
from models.bot_user import BotUser
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
        self.engine = create_engine(DSN)
        Session = sessionmaker(bind=self.engine)
        self._session = Session()
        Base.metadata.create_all(self.engine)
        self.user_states = {}
        self.current_state = None
        self.user_words = None
        self.target_word = None
        self.viewed_words = []

    def identified_user(self, user_id: int) -> int | None:
        with self._session as session:
            familiar = session.query(BotUser).filter(BotUser.id == user_id).first()
            print(familiar, familiar.id) if familiar else print(None)
            return familiar.id if familiar else None

    def _get_random_cards(self, user_id: int, amount=4):
        with self._session as session:
            random_words = session.query(Word).join(BotUser, Word.user_id == BotUser.id).filter(BotUser.id == user_id)\
                .order_by(sa.func.random()).limit(amount).all()
            return random_words

    def get_next_card(self, user_id: int) -> None:
        self.user_words = self._get_random_cards(user_id)
        self.target_word = self.user_words[0]
        self.viewed_words.append(self.target_word)

    def close(self):
        self._session.close()

    def init_default_cards(self, user_id: int) -> bool:
        try:
            with open('data_base/default_words.json') as file:
                default_words = json.load(file)
        except FileNotFoundError:
            print('File not found')
            return False
        models = {'bot_user': BotUser, 'word': Word, 'category': Category}
        words_list = []
        category_list = []
        category_word_list = []
        for line in default_words:
            model = models[line.get("model")]
            if line.get("model") == "word":
                words_list.append(Word(user_id=user_id, **line.get("fields")))
                category_word_list.append(CategoryWord(category_id=CATEGORY['COMMON'], word_id=line.get("pk")))
            elif line.get("model") == "category":
                category_list.append(Category(**line.get("fields")))
        with self._session as session:
            bot_user = BotUser(id=user_id, name="InnCent")
            session.add(bot_user)
            session.commit()
            session.add_all(words_list)
            session.flush()
            session.add_all(category_list)
            session.flush()
            session.add_all(category_word_list)
            session.commit()
        return True

    def _find_word(self, user_id: int, rus_title: str, eng_title: str) -> Word | None:
        eng_title = eng_title.lower().strip()
        rus_title = rus_title.lower().strip()
        with self._session as session:
            return session.query(Word).filter(Word.user_id == user_id)\
                .filter(Word.rus_title.ilike(f"{rus_title}")).filter(Word.eng_title.ilike(f"{eng_title}")).first()

    def _find_category(self, user_id: int, name: str) -> int | None:
        name = name.lower().strip()
        with self._session as session:
            category = session.query(Category).join(CategoryWord, Category.id == CategoryWord.category_id)\
                .join(Word, CategoryWord.word_id == Word.id)\
                .filter(Word.user_id == user_id).filter(Category.name.ilike(f"{name}")).first()
            return category.id if category else None

    def _check_new_word(self, user_id, word, eng=False) -> bool:
        word = word.lower().strip()
        if not eng:
            with self._session as session:
                pass
        else:
            return False

    def add_word(self, user_id, rus_title, eng_title, category="общие") -> bool:
        word_exist = self._find_word(user_id, rus_title, eng_title)
        if not word_exist:
            with self._session as session:
                new_word = Word(rus_title=rus_title, eng_title=eng_title, user_id=user_id)
                session.add(new_word)
                session.flush()
                new_category_word = []
                if category != "общие":
                    category_id = self._find_category(user_id, category)
                    if category_id is None:
                        new_category = Category(name=category)
                        session.add(new_category)
                        session.flush()
                        new_category_word.append(CategoryWord(category_id=new_category.id, word_id=new_word.id))
                    else:
                        new_category_word.append(CategoryWord(category_id=category_id, word_id=new_word.id))
                new_category_word.append(CategoryWord(category_id=CATEGORY['COMMON'], word_id=new_word.id))
                session.add_all(new_category_word)
                session.commit()
                return True
        return False

    def delete_word(self, user_id: int, word: str) -> bool:
        with self._session as session:
            word_exist = session.query(Word).filter(Word.user_id == user_id)\
                .filter(Word.rus_title.ilike(f"{word}") | Word.eng_title.ilike(f"{word}")).first()
        if word_exist:
            session.delete(word_exist)
            session.commit()
            return True
        else:
            return False
