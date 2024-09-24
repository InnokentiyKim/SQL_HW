import json
from bot_logging.bot_logging import error_logging, LOGGER_PATH
from models.bot_user import BotUser
from models.category import Category
from models.word import Word


def load_words_from_json(file_path: str, user: BotUser, categories: list[Category] = None) -> list[Word]:
    """
    Загружает список слов из JSON-файла.
    Параметры:
        file_path (str): Путь к JSON-файлу
        user (BotUser): Пользователь бота
        categories (list[Category], optional): Список категорий. Если задан, то все слова будут иметь заданную категорию.
    Возвращает:
        list[Word]: Список слов
    """
    with open (file_path, 'r', encoding='utf-8') as file:
        words_data = json.load(file)
        if categories:
            words_list = [Word(bot_user=user, **word, category=categories) for word in words_data]
        else:
            words_list = [Word(bot_user=user, **word) for word in words_data]
    return words_list
