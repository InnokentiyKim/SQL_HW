from settings.config import settings, COMMANDS, KEYBOARD


help = f"""
<b> добро пожаловать в телеграм бот "Learning English Vocabulary"!</b>
Данный бот был разработан чтобы помочь вам изучать английский язык по карточкам.

<i>Команды:</i>
-<b>({COMMANDS['START']}) - </b><i>старт</i>
-<b>({COMMANDS['CARDS']}) - </b><i>показать карточки слов</i>
-<b>({COMMANDS['PLAY']}) - </b><i>играть</i>

<i>Версия: </i><b>{settings.VERSION}</b>
<i>Автор: </i><b>{settings.AUTHOR}</b>
"""

info = f"""
<b> Общее руководство:</b>
<i> Навигация:</i>
-<b>({KEYBOARD['NEXT_STEP']}) - </b><i>следующее слово</i>
-<b>({KEYBOARD['BACK']}) - </b><i>назад</i>

<i>Специальные кнопки:</i>
-<b> {KEYBOARD['MENU']} </b>
-<b> {KEYBOARD['SETTINGS']} </b>
-<b> {KEYBOARD['ADD_WORD']} </b>
-<b> {KEYBOARD['DELETE_WORD']} </b>

<i>Общая информация:</i>
-<b>версия программы - </b><i>({settings.VERSION})</i>
-<b>разработчик - </b><i>({settings.AUTHOR})</i>

<b>{KEYBOARD['COPY']}<i>Иннокентий Ким</i></b>
"""

start = f"""
давай попрактикуемся в английском языке.
Тренировки можешь проходить в удобном для себя темпе.
Причём у тебя есть возможность использовать тренажёр как конструктор и собирать свою собственную базу для обучения. 
Для этого воспрользуйся инструментами {KEYBOARD['ADD_WORD']} или {KEYBOARD['DELETE_WORD']} в Меню бота.
"""

next_word = """
что в переводе означает слово: 
"""

add_word_eng = """
введите слово на английском языке:
"""

add_word_rus = """
введите слово на русском языке:
"""

add_category = """
введите категорию для нового слова:
"""

bot_description = f"""
Бот для изучения английского языка. Бот поможет вам 
изучить английский язык по карточкам. 
Версия бота: {settings.VERSION}
Автор: {settings.AUTHOR}{KEYBOARD['COPY']}
"""

MESSAGES = {
    'BOT_DESCRIPTION': bot_description,
    'HELP': help,
    'START': start,
    'NEXT_WORD': next_word,
    'INFO': info,
    'ADD_WORD_ENG': add_word_eng,
    'ADD_WORD_RUS': add_word_rus,
    'ADD_CATEGORY': add_category,
}
