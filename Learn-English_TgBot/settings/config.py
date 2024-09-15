import os
from emoji import emojize
from enum import Enum
from pydantic.v1 import BaseSettings, Field


class AdvancedBaseSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        allow_mutation = False


class Settings(AdvancedBaseSettings):
    TOKEN: str = Field(env='TOKEN')
    DB_NAME: str = Field(env='DB_NAME', default='postgres')
    DIALECT: str = Field(env='DIALECT', default='postgresql')
    USERNAME: str = Field(env='USERNAME', default='postgres')
    PASSWORD: str = Field(env='PASSWORD', default='postgres')
    PORT: int = Field(env='PORT', default=5432)
    URL: str = Field(env='URL', default='localhost')
    WORDS_URL: str = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    WORDS_LIMIT: int = 10
    TARGET_WORDS_CHUNK_SIZE: int = 10
    OTHER_WORDS_CHUNK_SIZE: int = 50
    WORDS_IN_CARDS: int = 4
    VERSION: str = '1.0.0'
    AUTHOR: str = 'InnCent'
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH: str = 'source/data/default_words.json'

    @property
    def DSN(self):
        return f"{self.DIALECT}://{self.USERNAME}:{self.PASSWORD}@{self.URL}:{self.PORT}/{self.DB_NAME}"


settings = Settings()


KEYBOARD = {
    'INFO': emojize("💬 INFO о боте"),
    'MENU': emojize("⚙ Меню"),
    'SETTINGS': emojize("🔧 Настройки"),
    'NEXT_STEP': emojize("➡ Дальше"),
    'ADD_WORD': emojize("➕ Добавить слово"),
    'DELETE_WORD': emojize("❌ Удалить слово"),
    'BACK': emojize("🔙 Назад"),
    'COPY': emojize(":copyright:"),
    'RUS': emojize("🇷🇺"),
    'ENG': emojize("🇺🇲")
}

KEYBOARD_NAMES = [name for name in KEYBOARD.keys()]

CATEGORIES = {
    'COMMON': {'value': 1, 'name': 'Общие'},
    'TRANSPORT': {'value': 2, 'name': 'Транспорт'},
    'ANIMALS': {'value': 3, 'name': 'Животные'},
    'CLOTHES': {'value': 4, 'name': 'Одежда'},
    'COLORS': {'value': 5, 'name': 'Цвета'}
}

COMMANDS = {
    'START': 'start',
    'HELP': 'help',
    'CARDS': 'cards',
    'PLAY': 'play',
}

MENU_COMMANDS = {
    'start': 'Начать',
    'help': 'Помощь',
    'cards': 'Карточки',
    'add_word': 'Добавить слово',
    'delete_word': 'Удалить слово',
    'settings': 'Настройки',
}


class TranslationMode(Enum):
    RUS_TO_ENG = 1
    ENG_TO_RUS = 2


class UserStates(Enum):
    START = 1
    PLAYING = 2
    ADDING_DATA = 3
    DELETING_DATA = 4
    CONFIGURING = 5
