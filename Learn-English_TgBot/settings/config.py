import os
from emoji import emojize
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

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
    'MENU': emojize(":gear: Меню"),
    'SETTINGS': emojize(":wrench: Настройки"),
    'NEXT_STEP': emojize(":right_arrow: Дальше"),
    'ADD_WORD': emojize(":plus: Добавить слово"),
    'DELETE_WORD': emojize(":minus: Удалить слово"),
    'BACK': emojize("🔙 Назад"),
    'COPY': emojize(":copyright:"),
    'RUS': emojize("🇷🇺"),
    'ENG': emojize("🇺🇲")
}

CATEGORY = {
    'COMMON': 1,
    'TRANSPORT': 2,
    'ANIMALS': 3,
    'CLOTHES': 4,
}

USER_STATES = {
    'START': 1,
    'PLAYING': 2,
    'ADDING_DATA': 3,
    'DELETING_DATA': 4,
    'CONFIGURING': 5,
}

COMMANDS = {
    'START': "start",
    'HELP': "help",
    'CARDS': "cards",
    'PLAY': "play",
}
