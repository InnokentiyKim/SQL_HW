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

start = """
давай попрактикуемся в английском языке.
Тренировки можешь проходить в удобном для себя темпе.
Причём у тебя есть возможность использовать тренажёр как конструктор 
и собирать свою собственную базу для обучения. Для этого воспрользуйся 
инструментами Добавить слово {} или Удалить слово {}.
""".format(
    KEYBOARD['ADD_WORD'],
    KEYBOARD['DELETE_WORD']
)

next_word = """
что в переводе означает слово: 
"""

MESSAGES = {
    'HELP': help,
    'START': start,
    'NEXT_WORD': next_word,
    'INFO': info,
    # 'settings': settings
}
