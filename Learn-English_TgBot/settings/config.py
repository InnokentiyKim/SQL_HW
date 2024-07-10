import os
from emoji import emojize

TOKEN = ''
DB_NAME = 'words'
VERSION = '1.0.0'
AUTHOR = 'InnCent'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATABASE = os.path.join('postgresql://'+BASE_DIR, DB_NAME)
DIALECT = 'postgresql'
USERNAME = ''
PASSWORD = ''
PORT = 5432
URL = 'localhost'
DSN = f"{DIALECT://{USERNAME}:{PASSWORD}@{URL}:{PORT}/{DB_NAME}}"

KEYBOARD = {
    'INFO': emojize(":speech_baloon: О боте 'Learning English Vocabulary'" ),
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