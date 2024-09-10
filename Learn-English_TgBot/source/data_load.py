from pydantic import TypeAdapter
from bot_logging.bot_logging import error_logging, LOGGER_PATH
import json
from models.category import Category
from models.category_word import CategoryWord
from models.word import Word
from source.data_models import WordDTO, CategoryDTO, CategoryWordDTO


@error_logging(path=LOGGER_PATH)
def load_data(file_path: str, ModelOrm, ModelDTO) -> list[object]:
    with open (file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    objects_list = []
    for row in data:
        if row.get('model') == ModelOrm.__name__:
            valid_row = TypeAdapter(ModelDTO).validate_python(row)
            objects_list.append(ModelOrm(**valid_row.model_dump(exclude={'model'})))
    return objects_list

def init_default_words(session, user_id: int) -> bool:
    default_words = load_data('source/default_words.json', Word, WordDTO)
    default_categories = load_data('source/default_words.json', Category, CategoryDTO)
    categories_words = load_data('source/default_words.json', CategoryWord, CategoryWordDTO)
    with session as sess:
        sess.add_all(default_categories).flush()
        sess.add_all(default_words).flush()
        sess.add_all(categories_words)
        sess.commit()
        return True
