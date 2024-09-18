import json

from pydantic import TypeAdapter
from bot_logging.bot_logging import error_logging, LOGGER_PATH
from models.bot_user import BotUser
from models.category import Category
from models.word import Word
from models.word_stats import WordStats
from source.data_models import WordDTO


@error_logging(path=LOGGER_PATH)
def load_words_from_json(file_path: str, user: BotUser, categories: list[Category] = None) -> list[Word]:
    with open (file_path, 'r', encoding='utf-8') as file:
        words_data = json.load(file)
        if categories:
            words_list = [Word(bot_user=user, **word, category=categories) for word in words_data]
        else:
            words_list = [Word(bot_user=user, **word) for word in words_data]
    return words_list
