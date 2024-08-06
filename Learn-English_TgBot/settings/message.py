from settings.config import VERSION, AUTHOR, COMMANDS, KEYBOARD


help = f"""
<b> добро пожаловать в телеграм бот "Learning English Vocabulary"!</b>
Данный бот был разработан чтобы помочь вам изучать английский язык по карточкам.

<i>Команды:</i>
-<b>({COMMANDS['START']}) - </b><i>старт</i>
-<b>({COMMANDS['CARDS']}) - </b><i>показать карточки слов</i>
-<b>({COMMANDS['PLAY']}) - </b><i>играть</i>

<i>Версия: </i><b>{VERSION}</b>
<i>Автор: </i><b>{AUTHOR}</b>
"""

info = f"""
<b> Общее руководство:</b>
<i> Навигация:</i>
-<b>({KEYBOARD['NEXT_STEP']}) - </b><i>следующее слово</i>
-<b>({KEYBOARD['BACK']}) - </b><i>назад</i>

<i>Специальные кнопки:</i>
-<b>({KEYBOARD['MENU']}) - </b><i>меню</i>
-<b>({KEYBOARD['SETTINGS']}) - </b><i>настройки</i>
-<b>({KEYBOARD['ADD_WORD']}) - </b><i>добавить слово</i>
-<b>({KEYBOARD['DELETE_WORD']}) - </b><i>удалить слово</i>

<i>Общая информация:</i>
-<b>версия программы - </b><i>({VERSION})</i>
-<b>разработчик - </b><i>({AUTHOR})</i>

<b>{KEYBOARD['COPY']}<i>Иннокентий Ким</i></b>
"""

start = f"""
давай попрактикуемся в английском языке.
Тренировки можешь проходить в удобном для себя темпе.
Причём у тебя есть возможность использовать тренажёр как конструктор 
и собирать свою собственную базу для обучения. Для этого воспрользуйся 
инструментами Добавить слово {KEYBOARD['ADD_WORD']} или Удалить слово {KEYBOARD['DELETE_WORD']}.
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

MESSAGES = {
    'HELP': help,
    'START': start,
    'NEXT_WORD': next_word,
    'INFO': info,
    'ADD_WORD_ENG': add_word_eng,
    'ADD_WORD_RUS': add_word_rus,
    'ADD_CATEGORU': add_category,
}
