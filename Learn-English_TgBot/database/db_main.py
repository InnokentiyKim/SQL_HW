from typing import cast
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql.operators import or_
from bot_logging.bot_logging import error_logging, LOGGER_PATH, error_logger
from database.db_core import Session, Singleton, Base
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
    """
    Менеджер базы данных.
    Реализует паттерн Singleton, гарантируя, что будет создан только один экземпляр класса.
    Предоставляет методы для взаимодействия с базой данных, включая добавление и удаление данных,
    получение информации о пользователях и их категориях.
    Атрибуты:
        _session: Сессия базы данных
    Методы:
        identify_user: Идентифицирует пользователя по его ID.
        format_title: Форматирует название категории или слова.
        add_new_user: Добавляет нового пользователя в базу данных.
        get_category_by_name: Возвращает категорию по ее имени.
        get_all_users_categories: Возвращает все категории пользователя.
        get_studying_words_count: Возвращает количество изучаемых слов пользователя.
        get_user_settings: Возвращает настройки пользователя.
        update_user_settings: Обновляет настройки пользователя.
        find_word: Находит слово по его названию.
        get_target_words: Возвращает список целевых слов для пользователя.
        get_other_words: Возвращает список других слов для пользователя.
        update_users_stats: Обновляет статистику пользователя.
        add_new_word: Добавляет новое слово в базу данных.
        delete_word: Удаляет слово из базы данных.
    """
    def __init__(self, engine):
        self._session = Session()
        Base.metadata.create_all(engine)

    @error_logging(path=LOGGER_PATH)
    def identify_user(self, user_id: int) -> BotUser | None:
        """
        Идентифицирует пользователя по его ID.
        Выполняет запрос в базу данных для получения информации о пользователе с указанным ID.
        Если пользователь найден, возвращает объект пользователя, иначе возвращает None.
        Аргументы:
            user_id (int): ID пользователя.
        Возвращает:
            BotUser | None: Объект пользователя или None, если пользователь не найден.
        """
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
        """
        Добавляет нового пользователя в базу данных.
        Выполняет запрос в базу данных для добавления нового пользователя с указанными данными.
        Если пользователь успешно добавлен, метод не возвращает ничего.
        Параметры:
            user_id (int): ID пользователя.
            username (str): Имя пользователя.
        Возвращает:
            None
        """
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
        except sa.exc.IntegrityError as integrity_error:
            error_logger.error(integrity_error)
        except Exception as error:
            error_logger.error(error)
        return None

    @error_logging(path=LOGGER_PATH)
    def get_category_by_name(self, user_id: int, name: str) -> Category | None:
        """
        Возвращает категорию по ее имени.
        Выполняет запрос в базу данных для получения категории с указанным именем для указанного пользователя.
        Если категория найдена, возвращает объект категории, иначе возвращает None.
        Параметры:
            user_id (int): ID пользователя.
            category_name (str): Имя категории.
        Возвращает:
            Category | None: Объект категории или None, если категория не найдена.
        """
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

    @error_logging(path=LOGGER_PATH)
    def get_all_users_categories(self, user_id: int) -> list[Category] | None:
        """
        Возвращает все категории пользователя.
        Выполняет запрос в базу данных для получения всех категорий, принадлежащих указанному пользователю.
        Возвращает список объектов категорий.
        Параметры:
            user_id (int): ID пользователя.
        Возвращает:
            list[Category]: Список объектов категорий или None, если категории не найдены.
        """
        with self._session as session:
            query = (
                sa.select(Category)
                .options(selectinload(Category.word))
                .filter(cast("ColumnElement[bool]", Word.user_id == user_id))
            )
            categories = session.execute(query).unique().scalars().all()
        return categories

    @error_logging(path=LOGGER_PATH)
    def get_studying_words_count(self, user_id: int) -> int:
        """
        Возвращает количество изучаемых слов пользователя.
        Выполняет запрос в базу данных для получения количества слов, которые пользователь в настоящее время изучает.
        Возвращает целое число, представляющее количество слов.
        Параметры:
            user_id (int): ID пользователя.
        Возвращает:
            int: Количество изучаемых слов.
        """
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

    @error_logging(path=LOGGER_PATH)
    def get_user_settings(self, user_id: int) -> UserSettings | None:
        """
       Возвращает настройки пользователя.
       Выполняет запрос в базу данных для получения настроек пользователя с указанным ID.
       Возвращает объект настроек пользователя.
       Параметры:
           user_id (int): ID пользователя.
       Возвращает:
           UserSettings: Объект настроек пользователя или None, если настройки не найдены.
       """
        with self._session as session:
            cur_settings = session.get(UserSettings, user_id)
            return cur_settings

    def update_user_settings(self, user: BotUser) -> bool:
        """
        Обновляет настройки пользователя.
        Выполняет запрос в базу данных для обновления настроек пользователя с указанным ID.
        Обновляет настройки пользователя в соответствии с переданными данными.
        Параметры:
            user (BotUser): Объект пользователя.
        Returns:
            bool: True, если обновление прошло успешно, False в противном случае.
        """
        try:
            with self._session as session:
                session.add(user)
                session.commit()
                return True
        except Exception as error:
            error_logger.error(error)
        return False

    @error_logging(path=LOGGER_PATH)
    def find_word(self, user_id: int, words_title: str) -> Word | None:
        """
        Находит слово по его названию.
        Выполняет запрос в базу данных для поиска слова с указанным названием.
        Если слово найдено, возвращает объект слова, иначе возвращает None.
        Параметры:
            user_id (int): ID пользователя.
            word_title (str): Название слова.
        Возвращает:
            Word | None: Объект слова или None, если слово не найдено.
        """
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

    @error_logging(path=LOGGER_PATH)
    def get_target_words(self, user_id: int, category: str = CATEGORIES['COMMON']['name'],
                          amount: int = settings.TARGET_WORDS_CHUNK_SIZE, is_studied: int = 0) -> list[Word]:
        """
        Возвращает список целевых слов для пользователя.
        Выполняет запрос в базу данных для получения списка слов, которые пользователь должен изучить в указанной категории.
        Возвращает список объектов слов.
        Параметры:
            user_id (int): ID пользователя.
            category (str): Название категории.
            amount (int): Количество слов.
            is_studied (int): Признак изученного слова.
        Возвращает:
            list[Word]: Список объектов слов.
        """
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

    @error_logging(path=LOGGER_PATH)
    def get_other_words(self, user_id: int, category: str = CATEGORIES['COMMON']['name'],
                        amount: int = settings.OTHER_WORDS_CHUNK_SIZE) -> list[Word]:
        """
        Возвращает список других слов пользователя для формирования карточек слов.
        Выполняет запрос в базу данных для получения списка слов, которые не являются целевыми.
        Возвращает список объектов слов.
        Параметры:
            user_id (int): ID пользователя.
            category_id (int): ID категории.
        Возвращает:
            list[Word]: Список объектов слов.
        """
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
        """
        Выполняет запрос в базу данных для обновления статистики пользователя.
        Также обновляет статику каждого слова.
        Параметры:
            user (BotUser): Объект пользователя.
            words (list[Word]): Список объектов слов.
        Возвращает:
            bool: True, если обновление прошло успешно, False в противном случае.
        """
        if user and words:
            try:
                with self._session as session:
                    session.add(user)
                    word_stats = [word.word_stats for word in words]
                    session.add_all(word_stats)
                    session.commit()
                return True
            except IntegrityError as integrity_error:
                error_logger.error(integrity_error)
            except Exception as error:
                error_logger.error(error)
        return False

    def add_new_word(self, user: BotUser, rus_title, eng_title, category_name = CATEGORIES['COMMON']['name']) -> bool:
        """
        Добавляет новое слово в базу данных.
        Выполняет запрос в базу данных для добавления нового слова с указанными данными.
        Добавляет новое слово в указанную категорию (если такая категория не существует, то создает ее)
        Одновременно добавляет слово в общую категорию.
        Параметры:
            user (BotUser): Объект пользователя.
            rus_title (str): Русское название слова.
            eng_title (str): Английское название слова.
            category_name (str): Название категории (по умолчанию COMMON)
        Возвращает:
            bool: True, если добавление прошло успешно, False в противном случае.
        """
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
        except sa.exc.IntegrityError as integrity_error:
            error_logger.error(integrity_error)
        except Exception as error:
            error_logger.error(error)
        return False

    def delete_word(self, user: BotUser, word: str) -> bool:
        """
        Удаляет слово из базы данных.
        Выполняет запрос в базу данных для удаления слова по названию (русскому или английскому).
        Удаляет слово и все связанные с ним данные.
        Параметры:
            user (BotUser): Объект пользователя.
            word (str): Название слова.
        Возвращает:
            bool: True, если удаление прошло успешно, False в противном случае.
        """
        try:
            with self._session as session:
                deleting_word = self.find_word(user_id=user.id, words_title=word)
                if deleting_word:
                    session.delete(deleting_word)
                    session.commit()
                    return True
        except sa.exc.IntegrityError as integrity_error:
            error_logger.error(integrity_error)
        except Exception as error:
            error_logger.error(error)
        return False

    def delete_category(self, user: BotUser, category_name: str) -> bool:
        """
        Удаляет категорию из базы данных.
        Выполняет запрос в базу данных для удаления категории с указанным названием.
        Удаляет категорию и все связанные с ней данные.
        Параметры:
            user (BotUser): Объект пользователя.
            category_name (str): Название категории.
        Возвращает:
            bool: True, если удаление прошло успешно, False в противном случае.
        """
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
        except sa.exc.IntegrityError as integrity_error:
            error_logger.error(integrity_error)
        except Exception as error:
            error_logger.error(error)
        return False
