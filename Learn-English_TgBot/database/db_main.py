from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql.operators import or_
from database.db_core import Session, Singleton, Base, engine
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
    def __init__(self):
        self._session = Session()
        Base.metadata.create_all(engine)

    def identify_user(self, user_id: int) -> int | None:
        with self._session as session:
            query = (
                sa.select(BotUser)
                .filter(BotUser.id == user_id)
                .options(selectinload(BotUser.user_stats))
                .options(selectinload(BotUser.user_settings))
            )
            familiar_user = session.execute(query).scalars().first()
            return familiar_user if familiar_user else None

    def add_new_user(self, user_id: int, user_name: str = '') -> BotUser | None:
        new_user = BotUser(id=user_id, name=user_name)
        try:
            with self._session as session:
                session.add(new_user).flush()
                user_stats = UserStats(bot_user=new_user)
                user_settings = UserSettings(bot_user=new_user)
                base_category = Category()
                session.add_all([user_stats, user_settings, base_category]).flush()
                words = load_words_from_json(settings.DATA_PATH,  new_user, [base_category])
                session.add_all(words).flush()
                words_stats = [WordStats(word=word) for word in words]
                session.add_all(words_stats)
                session.commit()
                return new_user
        except sa.exc.IntegrityError:
            pass
        except sa.exc.UniqueViolation:
            pass
        except Exception as error:
            pass
        return None

    def get_category_by_name(self, user_id: int, name: str) -> Category | None:
        name = name.capitalize().strip()
        with self._session as session:
            query = (
                sa.select(Category).filter(Category.name.ilike(f"{name}"))
                .options(selectinload(Category.word))
                .filter(Word.user_id == user_id).first()
            )
            category = session.execute(query).scalars().first()
        return category if category else None

    def find_words(self, user_id: int, words_title: str) -> list[Word] | None:
        words_title = words_title.capitalize().strip()
        with self._session as session:
            query = (
                sa.select(Word).filter(Word.user_id == user_id)
                .filter(or_(Word.rus_title.ilike(f"{words_title}"), Word.eng_title.ilike(f"{words_title}")))
            )
            word = session.execute(query).scalars().all()
        return word

    def get_target_words(self, user_id: int, category: str = CATEGORIES['COMMON']['name'],
                          amount: int = settings.TARGET_WORDS_CHUNK_SIZE, is_studied: int = 0) -> list[Word]:
        category = category.capitalize().strip()
        query = (
            sa.select(Word).filter(Word.user_id == user_id)
            .options(selectinload(Word.category))
            .options(joinedload(Word.word_stats))
            .filter(Category.name == category)
            .filter(WordStats.is_studied == is_studied)
            .order_by(sa.func.random())
            .limit(amount)
        )
        with self._session as session:
            target_words = session.execute(query).scalars().all()
        return target_words

    def get_other_words(self, user_id: int, category: str = CATEGORIES['COMMON']['name'],
                          amount: int = settings.OTHER_WORDS_CHUNK_SIZE) -> list[Word]:
        category = category.capitalize().strip()
        query = (
            sa.select(Word).filter(Word.user_id == user_id)
            .options(selectinload(Word.category))
            .filter(Category.name == category)
            .order_by(sa.func.random())
            .limit(amount)
        )
        with self._session as session:
            other_words = session.execute(query).scalars().all()
        return other_words

    def check_new_word(self, user_id, word: str) -> bool:
        word = word.capitalize().strip()
        with self._session as session:
            query = (
                sa.select(Word).filter(Word.user_id == user_id)
                .filter(or_(Word.rus_title.ilike(f'{word}'), Word.eng_title.ilike(f'{word}')))
            )
            selected_word = session.execute(query).scalars().first()
        return selected_word is not None

    def add_new_word(self, user: BotUser, rus_title, eng_title, category_name = CATEGORIES['COMMON']['name']) -> bool:
        try:
            category = self.get_category_by_name(user.id, category_name)
            if not category:
                return False
            word_stats = WordStats()
            new_word = Word(rus_title=rus_title, eng_title=eng_title, user=user, category=[category], word_stats=word_stats)
            with self._session as session:
                session.add(new_word).commit()
            return True
        except sa.exc.IntegrityError:
            return False
        except sa.exc.UniqueViolation:
            return False
        except Exception as error:
            return False

    def delete_word(self, user_id: int, word: str) -> bool:
        try:
            with self._session as session:
                deleting_words = self.find_words(user_id, word)
                if not deleting_words:
                    return False
                for word in deleting_words:
                    session.delete(word)
                session.commit()
            return True
        except Exception as error:
            return False
