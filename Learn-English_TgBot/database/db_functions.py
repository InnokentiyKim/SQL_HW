import requests
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql.operators import or_
from database.db_core import Session
from models.user_settings import UserSettings
from models.user_stats import UserStats
from models.category import Category
from models.bot_user import BotUser
from models.word import Word
from models.word_stats import WordStats
from settings.config import settings, CATEGORIES
from source.data_load import load_words_from_json
from source.data_models import UsersPlaySession
import sqlalchemy as sa


class DBFunctions:
    def __init__(self):
        self._session = Session()
        self.play_session = UsersPlaySession()
        self.words_api_url = settings.WORDS_URL

    def _identify_user(self, user_id: int) -> int | None:
        with self._session as session:
            familiar = session.query(BotUser).filter(BotUser.id == user_id).first()
            return familiar.id if familiar else None

    def _add_new_user(self, user_id: int, user_name: str = '') -> bool:
        new_user = BotUser(id=user_id, name=user_name)
        try:
            with self._session as session:
                session.add(new_user).flush()
                user_settings = UserSettings(bot_user=new_user)
                user_stats = UserStats(bot_user=new_user)
                base_category = Category()
                session.add_all([user_settings, user_stats, base_category]).flush()
                words = load_words_from_json(settings.DATA_PATH, new_user, [base_category])
                session.add(words).flush()
                words_stats = [WordStats(word=word) for word in words]
                session.add_all(words_stats)
                session.commit()
        except sa.exc.IntegrityError:
            return False
        except sa.exc.UniqueViolation:
            return False
        except Exception as error:
            return False
        return True

    def _find_category(self, user_id: int, name: str) -> int | None:
        name = name.capitalize().strip()
        with self._session as session:
            query = (
                select(Category).filter(Category.name.ilike(f"{name}"))
                .options(selectinload(Category.word))
                .filter(Word.user_id == user_id).first()
            )
            category = session.execute(query).scalars().first()
        return category.id if category else None

    def _find_word(self, user_id: int, rus_title: str, eng_title: str) -> Word | None:
        eng_title = eng_title.capitalize().strip()
        rus_title = rus_title.capitalize().strip()
        with self._session as session:
            query = (
                select(Word).filter(Word.user_id == user_id)
                .filter(Word.rus_title.ilike(f"{rus_title}"))
                .filter(Word.eng_title.ilike(f"{eng_title}"))
            )
            word = session.execute(query).scalars().first()
        return word

    def _check_new_word(self, user_id, word: str) -> bool:
        word = word.capitalize().strip()
        with self._session as session:
            query = (
                select(Word).filter(Word.user_id == user_id)
                .filter(or_(Word.rus_title.ilike(f'{word}'), Word.eng_title.ilike(f'{word}')))
            )
            selected_word = session.execute(query).scalars().first()
        return selected_word is not None

    def _get_target_words(self, user_id: int, category: str = CATEGORIES['COMMON']['name'],
                          amount: int = settings.TARGET_WORDS_CHUNK_SIZE, is_studied: int = 0) -> list[Word]:
        category = category.capitalize().strip()
        self.id = Word.user_id == user_id
        query = (
            select(Word).filter(Word.user_id == user_id)
            .options(selectinload(Word.category))
            .options(joinedload(Word.word_stats))
            .filter(Category.name == category)
            .filter(WordStats.is_studied == is_studied)
            .limit(amount)
        )
        with self._session as session:
            target_words = session.execute(query).scalars().all()
        return target_words




    def _get_random_cards(self, user_id: int, chunk_size=4):
        with self._session as session:
            random_words = (
                session.query(Word)
                .join(BotUser, Word.user_id == BotUser.id)
                .filter(BotUser.id == user_id)
                .order_by(sa.func.random())
                .limit(chunk_size).all()
            )
        return random_words

    def get_words_description(self, word: str) -> dict:
        response = requests.get(self.words_api_url, params={'words': word}).json()
        description = response['description']
        return description

    def get_next_card(self, user_id: int) -> None:
        self.user_words = self._get_random_cards(user_id)
        self.target_word = self.user_words[0]
        self.viewed_words.append(self.target_word)
