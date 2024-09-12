from database.db_core import Base, Session, engine
from models.user_settings import UserSettings
from models.user_stats import UserStats
from models.category import Category
from models.bot_user import BotUser
from models.word import Word
from models.category_word import CategoryWord
from models.word_stats import WordStats
from settings.config import settings
from source.data_load import load_words_from_json
import sqlalchemy as sa


class DBFunctions:
    def __init__(self):
        self._session = Session()
        Base.metadata.create_all(engine)
        self.user_states = {}
        self.user_words = None
        self.target_word = None
        self.is_answered = False
        self.viewed_words = []

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
        name = name.lower().strip()
        with self._session as session:
            category = session.query(Category).join(CategoryWord, Category.id == CategoryWord.category_id) \
                .join(Word, CategoryWord.word_id == Word.id) \
                .filter(Word.user_id == user_id).filter(Category.name.ilike(f"{name}")).first()
            return category.id if category else None

    def _find_word(self, user_id: int, rus_title: str, eng_title: str) -> Word | None:
        eng_title = eng_title.capitalize().strip()
        rus_title = rus_title.capitalize().strip()
        with self._session as session:
            return session.query(Word).filter(Word.user_id == user_id) \
                .filter(Word.rus_title.ilike(f"{rus_title}")).filter(Word.eng_title.ilike(f"{eng_title}")).first()

    def _check_new_word(self, user_id, word, eng=False) -> bool:
        word = word.lower().strip()
        if not eng:
            with self._session as session:
                pass
        else:
            return False

    def _get_random_cards(self, user_id: int, word_amount=4, chunk_size=4):
        with self._session as session:
            random_words = (
                session.query(Word)
                .join(BotUser, Word.user_id == BotUser.id)
                .filter(BotUser.id == user_id)
                .order_by(sa.func.random())
                .limit(chunk_size).all()
            )
        return random_words

    def get_next_card(self, user_id: int) -> None:
        self.user_words = self._get_random_cards(user_id)
        self.target_word = self.user_words[0]
        self.viewed_words.append(self.target_word)

    def close(self):
        self._session.close()

    def add_word(self, user_id, rus_title, eng_title, category="общие") -> bool:
        existing_word = self._find_word(user_id, rus_title, eng_title)
        if not existing_word:
            with self._session as session:
                new_word = Word(rus_title=rus_title, eng_title=eng_title, user_id=user_id)
                session.add(new_word)
                session.flush()
                if category != "общие":
                    category_id = self._find_category(user_id, category)
                    if not category_id:
                        new_category = Category(name=category)
                        session.add(new_category)
                        session.flush()
                        new_category_word = CategoryWord(category_id=new_category.id, word_id=new_word.id)
                        session.add(new_category_word)
                    else:
                        new_category_word = (CategoryWord(category_id=category_id, word_id=new_word.id))
                        session.add(new_category_word)
                session.commit()
                extra_category_word = (CategoryWord(category_id=CategoryMode.COMMON.value, word_id=new_word.id))
                session.add(extra_category_word)
                session.commit()
                return True
        return False

    def delete_word(self, user_id: int, word: str) -> bool:
        with self._session as session:
            existing_word = session.query(Word).filter(Word.user_id == user_id) \
                .filter(Word.rus_title.ilike(f"{word}") | Word.eng_title.ilike(f"{word}")).first()
            if existing_word:
                session.delete(existing_word)
                session.commit()
                return True
        return False