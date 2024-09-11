import os
from emoji import emojize
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings
from enum import Enum

load_dotenv()


class Settings(BaseSettings):
    TOKEN = os.getenv('TOKEN')
    DB_NAME = os.getenv('DB_NAME')
    DIALECT = os.getenv('DIALECT')
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    PORT = os.getenv('PORT')
    URL = os.getenv('URL')
    WORDS_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    WORDS_LIMIT = 10
    VERSION = '1.0.0'
    AUTHOR = 'InnCent'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

COMMANDS = {
    'START': "start",
    'HELP': "help",
    'CARDS': "cards",
    'PLAY': "play",
}

class TranslationMode(Enum):
    RUS_TO_ENG = 1
    ENG_TO_RUS = 2

class CategoryMode(Enum):
    COMMON = (1, "Общие")
    TRANSPORT = (2, "Транспорт")
    ANIMALS = (3, "Животные")
    CLOTHES = (4, "Одежда")
    COLORS = (5, "Цвета")

class UserStates(Enum):
    START = 1
    PLAYING = 2
    ADDING_DATA = 3
    DELETING_DATA = 4
    CONFIGURING = 5
