import os
from emoji import emojize
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
DB_NAME = os.getenv('DB_NAME')
DIALECT = os.getenv('DIALECT')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')
URL = os.getenv('URL')
VERSION = '1.0.0'
AUTHOR = 'InnCent'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DSN = f"{DIALECT}://{USERNAME}:{PASSWORD}@{URL}:{PORT}/{DB_NAME}"

KEYBOARD = {
    'INFO': emojize(":speech_baloon: О боте 'Learning English Vocabulary'"),
    'SETTINGS': emojize(':gear: Настройки'),
    'NEXT_STEP': emojize(':right_arrow: Дальше'),
    'ADD_WORD': emojize(':plus: Добавить слово', variant='emoji_type'),
    'DELETE_WORD': emojize(':minus: Удалить слово',),
    'EXIT': emojize(':cross_mark: Выход'),
    'RUS': emojize(':flag_russia:'),
    'ENG': emojize(':🇺🇲:')
}

CATEGORY = {
    'COMMON': 1,
    'ANIMALS': 2,
    'COUNTRIES': 3
}

COMMANDS = {
    'START': "start",
    'HELP': "help",
    'CARDS': "cards",
    'PLAY': "play"
}
