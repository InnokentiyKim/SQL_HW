from pydantic import TypeAdapter
from bot_logging.bot_logging import error_logging, LOGGER_PATH
import json


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

default_words = load_data('source/default_words.json', Word, WordDTO)
default_categories = load_data('source/default_words.json', Category, CategoryDTO)
categories_words = load_data('source/default_words.json', CategoryWord, CategoryWordDTO)
