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
    WORDS_IN_CARDS: int = 4
    IS_STUDIED_COND: int = 5
    MIN_WORDS_CHUNK_SIZE: int = 1
    TARGET_WORDS_CHUNK_SIZE: int = 10
    OTHER_WORDS_CHUNK_SIZE: int = 5 * TARGET_WORDS_CHUNK_SIZE
    VERSION: str = '1.0.0'
    AUTHOR: str = 'InnCent'
    BOT_NAME: str = 'LearnEnglishVocabularyBot'
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    PIC_DIR: str = BASE_DIR + 'images/learn_english_bot.png'
    DATA_PATH: str = 'source/data/default_words.json'

    @property
    def DSN(self):
        return f"{self.DIALECT}://{self.USERNAME}:{self.PASSWORD}@{self.URL}:{self.PORT}/{self.DB_NAME}"


settings = Settings()


KEYBOARD = {
    'INFO': emojize("💬 INFO о боте"),
    'HINT': emojize("📖 Подсказка"),
    'MENU': emojize("⚙ Меню"),
    'SETTINGS': emojize("🔧 Настройки"),
    'NEXT_STEP': emojize("➡ Дальше"),
    'ADD_WORD': emojize("➕ Добавить слово"),
    'DELETE_WORD': emojize("❌ Удалить слово"),
    'USER_STATISTICS': emojize("📊 Статистика"),
    'BACK': emojize("🔙 Назад"),
    'COPY': emojize(":copyright:"),
    'NOTIFICATION': "Вкл/Выкл напоминания",
    'TRANSLATION_MODE': "Изменить режим перевода",
    'WORDS_CHUNK_SIZE': "Изменить количество слов раунда",
    'RESET_SETTINGS': "Сброс настроек",
    'RUS': emojize("🇷🇺"),
    'ENG': emojize("🇺🇲"),
}

NAVIGATION_KEYBOARD = [
    KEYBOARD['SETTINGS'],
    KEYBOARD['USER_STATISTICS'],
    KEYBOARD['HINT'],
    KEYBOARD['NEXT_STEP'],
]

SETTINGS_KEYBOARD = [
    KEYBOARD['NOTIFICATION'],
    KEYBOARD['TRANSLATION_MODE'],
    KEYBOARD['WORDS_CHUNK_SIZE'],
    KEYBOARD['RESET_SETTINGS'],
]

KEYBOARD_NAMES = [name for name in KEYBOARD.keys()]

ALIASES = {
    'BASIC': ['all', 'все'],
}

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
    'ADD_WORD': 'add_word',
    'DELETE_WORD': 'delete_word',
    'INFO': 'info',
}

MENU_COMMANDS = {
    "/start": "Начать",
    "/help": "Помощь",
    "/add_word": "Добавить слово",
    "/delete_word": "Удалить слово",
    "/info": "О боте",
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
