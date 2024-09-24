from typing import cast
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql.operators import or_
from database.db_core import Session, Singleton, Base
from models.category_word import CategoryWord
from models.user_settings import UserSettings
from models.user_stats import UserStats
from models.category import Category
from models.bot_user import BotUser
from models.word import Word
from models.word_stats import WordStats
from settings.config import settings, CATEGORIES
from source.data_load import load_words_from_json
import sqlalchemy as sa


class DBManager(metaclass=Singleton):
    def __init__(self, engine):
        self._session = Session()
        Base.metadata.create_all(engine)

    def identify_user(self, user_id: int) -> int | None:
        with self._session as session:
            query = (
                sa.select(BotUser)
                .filter(cast("ColumnElement[bool]", BotUser.id == user_id))
                .options(selectinload(BotUser.user_stats))
                .options(selectinload(BotUser.user_settings))
            )
            familiar_user = session.execute(query).scalars().first()
            return familiar_user if familiar_user else None

    @staticmethod
    def format_title(title: str) -> str:
        new_title = title.replace('_', ' ').strip().capitalize()
        return new_title

    def add_new_user(self, user_id: int, user_name: str = '') -> BotUser | None:
        new_user = BotUser(id=user_id, name=user_name)
        try:
            with self._session as session:
                session.add(new_user)
                session.flush()
                user_stats = UserStats(bot_user=new_user)
                user_settings = UserSettings(bot_user=new_user)
                base_category = Category()
                session.add_all([user_stats, user_settings])
                session.add(base_category)
                session.flush()
                words = load_words_from_json(settings.DATA_PATH, user=new_user)
                for word in words:
                    word.category = [base_category]
                session.add_all(words)
                session.flush()
                words_stats = [WordStats(word=word) for word in words]
                session.add_all(words_stats)
                session.commit()
                return new_user
        except sa.exc.IntegrityError:
            pass
        except Exception as error:
            pass
        return None

    def get_category_by_name(self, user_id: int, name: str) -> Category | None:
        name = self.format_title(name)
        with self._session as session:
            query = (
                sa.select(Category)
                .filter(Category.name.ilike(f"{name}"))
                .options(selectinload(Category.word))
                .filter(cast("ColumnElement[bool]", Word.user_id == user_id))
            )
            category = session.execute(query).scalars().first()
        return category

    def get_all_users_categories(self, user_id: int) -> list[Category] | None:
        with self._session as session:
            query = (
                sa.select(Category)
                .options(selectinload(Category.word))
                .filter(cast("ColumnElement[bool]", Word.user_id == user_id))
            )
            categories = session.execute(query).unique().scalars().all()
        return categories

    def get_studying_words_count(self, user_id: int) -> int:
        with self._session as session:
            query = (
                session.query(Word)
                .join(WordStats, Word.id == WordStats.word_id)
                .filter(Word.user_id == user_id)
                .filter(WordStats.is_studied == 0)
            )
            query = query.with_entities(sa.func.count())
            words_count = query.scalar()
        return words_count

    def get_user_settings(self, user_id: int) -> UserSettings | None:
        with self._session as session:
            cur_settings = session.get(UserSettings, user_id)
            return cur_settings

    def update_user_settings(self, user: BotUser) -> bool | None:
        with self._session as session:
            session.add(user)
            session.commit()
            return True

    def find_word(self, user_id: int, words_title: str) -> Word | None:
        words_title = self.format_title(title=words_title)
        with self._session as session:
            query = (
                sa.select(Word)
                .options(selectinload(Word.category))
                .filter(cast("ColumnElement[bool]", Word.user_id == user_id))
                .filter(or_(Word.rus_title.ilike(f"{words_title}"), Word.eng_title.ilike(f"{words_title}")))
            )
            found_word = session.execute(query).scalars().first()
        return found_word

    def get_target_words(self, user_id: int, category: str = CATEGORIES['COMMON']['name'],
                          amount: int = settings.TARGET_WORDS_CHUNK_SIZE, is_studied: int = 0) -> list[Word]:
        category = self.format_title(category)
        query = (
            sa.select(Word)
            .options(joinedload(Word.bot_user))
            .options(joinedload(Word.word_stats))
            .options(selectinload(Word.category))
            .filter(cast("ColumnElement[bool]", BotUser.id == user_id))
            .filter(cast("ColumnElement[bool]", WordStats.is_studied == is_studied))
            .filter(cast("ColumnElement[bool]", Category.name == category))
            .order_by(sa.func.random())
            .limit(amount)
        )
        with self._session as session:
            target_words = session.execute(query).unique().scalars().all()
        return target_words

    def get_other_words(self, user_id: int, category: str = CATEGORIES['COMMON']['name'],
                        amount: int = settings.OTHER_WORDS_CHUNK_SIZE) -> list[Word]:
        category = self.format_title(category)
        query = (
            sa.select(Word)
            .filter(cast("ColumnElement[bool]", Word.user_id == user_id))
            .options(joinedload(Word.word_stats))
            .options(selectinload(Word.category))
            .filter(cast("ColumnElement[bool]", Category.name == category))
            .order_by(sa.func.random())
            .limit(amount)
        )
        with self._session as session:
            other_words = session.execute(query).unique().scalars().all()
        return other_words

    def update_users_stats(self, user: BotUser, words: list[Word]) -> bool:
        if user and words:
            try:
                with self._session as session:
                    session.add(user)
                    session.add_all(words)
                    session.commit()
                return True
            except Exception as error:
                pass
        return False

    def add_new_word(self, user: BotUser, rus_title, eng_title, category_name = CATEGORIES['COMMON']['name']) -> bool:
        try:
            rus_title = self.format_title(rus_title)
            eng_title = self.format_title(eng_title)
            category_name = self.format_title(category_name)
            category_list = []
            if category_name != CATEGORIES['COMMON']['name']:
                base_category = self.get_category_by_name(user_id=user.id, name=CATEGORIES['COMMON']['name'])
                category_list.append(base_category)
            category = self.get_category_by_name(user_id=user.id, name=category_name)
            if not category:
                category = Category(name=category_name)
            category_list.append(category)
            new_word = Word(rus_title=rus_title, eng_title=eng_title, bot_user=user)
            with self._session as session:
                session.add_all(category_list)
                session.flush()
                new_word.category = category_list
                session.add(new_word)
                session.flush()
                new_word_stats = WordStats(word=new_word)
                session.add(new_word_stats)
                session.commit()
            return True
        except sa.exc.IntegrityError:
            pass
        except Exception as error:
            pass
        return False

    def delete_word(self, user: BotUser, word: str) -> bool:
        try:
            with self._session as session:
                deleting_word = self.find_word(user_id=user.id, words_title=word)
                if deleting_word:
                    session.delete(deleting_word)
                    session.commit()
                    return True
        except sa.exc.IntegrityError:
            pass
        except Exception as error:
            pass
        return False

    def delete_category(self, user: BotUser, category_name: str) -> bool:
        category = self.format_title(category_name)
        if category == CATEGORIES['COMMON']['name']:
            return False
        try:
            with self._session as session:
                deleting_category = self.get_category_by_name(user.id, category)
                if deleting_category:
                    session.delete(deleting_category)
                    session.commit()
            return True
        except sa.exc.IntegrityError:
            pass
        except Exception as error:
            pass
        return False

