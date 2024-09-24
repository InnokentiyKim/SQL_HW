from settings.config import settings, COMMANDS, KEYBOARD

help = f"""
<b> Добро пожаловать в телеграм бот "Learning English Vocabulary"!</b>
<b>Данный бот поможет вам изучить английский язык по карточкам.</b>

<i>Команды:</i>
-<b>({COMMANDS['START']}) - </b><i>🚀 Начать</i>
-<b>({COMMANDS['HELP']}) - </b><i>🆘 Помощь</i>
-<b>({COMMANDS['CARDS']}) - </b><i>🔠 Показать карточки слов</i>
-<b>({COMMANDS['ADD_WORD']}) - </b><i>➕ Добавить новое слово</i>
-<b>({COMMANDS['DELETE_WORD']}) - </b><i>❌ Удалить слово</i>
-<b>({COMMANDS['INFO']}) - </b><i>💬 Информация о боте</i>

<i> Основные клавиши:</i>
-<b>({KEYBOARD['NEXT_STEP']}) - </b><i>➡ Следующее слово</i>
-<b>({KEYBOARD['SETTINGS']}) - </b><i>🔧 Настройки бота</i>
-<b>({KEYBOARD['USER_STATISTICS']}) - </b><i>📊 Статистика пользователя</i>
-<b>({KEYBOARD['HINT']}) - </b><i>📖 Подсказка</i>

<i> Настройки:</i>
-<b>(🔔 {KEYBOARD['NOTIFICATION']})</b>
-<b>(🔠 {KEYBOARD['TRANSLATION_MODE']})</b>
-<b>(📚 {KEYBOARD['WORDS_CHUNK_SIZE']})</b>
-<b>(🔄 {KEYBOARD['RESET_SETTINGS']})</b>

Удачи в изучении английского языка!
"""

info = f"""
<b>Общая информация 📝:</b>
<i>Бот для изучения английского языка 🇺🇸</i>
<i>Бот поможет вам изучить английский язык по карточкам 🔠</i>
<i>Работать с ботом легко и удобно 🍸</i>
<i>Процесс тренировки построен в виде игры 🎮</i>
<i>Игра состоит из раундов по несколько карточек 🔥</i>
<i>Результаты каждого раунда учитываются в статистике 📊</i>
<i>В процессе тренировок вы можете взять подсказки 🤓</i>

Версия бота: {settings.VERSION}
Автор: {settings.AUTHOR}{KEYBOARD['COPY']}
"""

start = f""", давай попрактикуемся в английском языке 🇺🇸.
Тренировки можешь проходить в удобном для себя темпе 🚀.
Причём у тебя есть возможность использовать тренажёр как конструктор 🤖 и собирать свою собственную базу для обучения 🤔. 
Для этого воспрользуйся инструментами {KEYBOARD['ADD_WORD']} или {KEYBOARD['DELETE_WORD']} в {KEYBOARD['MENU']} бота.
"""

welcome = ", привет👋  Будем знакомы! 🤝"

welcome_back = ", c возвращением! 🎉 Рада видеть вас снова! 🤩"

lets_start = """
Чтобы начать 🚀 введите 👉 команду /cards
"""

end_round = f"""
Раунд закончен. Нажмите {KEYBOARD['NEXT_STEP']} чтобы начать новый
"""

round_results = f"""
<b>🏁 Результаты раунда 🏁</b>
"""

notification_on = """
Напоминания включены 🔔
"""

notification_off = """
Напоминания выключены 🔕
"""

eng_to_rus = """
Перевод с английского 🇺🇸 на русский 🇷🇺
"""

rus_to_eng = """
Перевод с русского 🇷🇺 на английский 🇺🇸
"""

words_amount = "Количество 🔢 слов в раунде 🏆"

change_words_amount = """
Количество 🔢 слов раунда 🏆 изменено на
"""

wrong_amount = """
Задано некорректное число слов 🚫. Настройки 🔧 не изменены 🚨
"""

reset_success = """
Все настройки 🔧 сброшены 🔃
"""

reset_failed = """
Не удалось 🚫 сбросить настройки 🔧
"""

hint = """
Подсказка 📖:
"""

no_hint = """
К сожалению подсказка 📖 недоступна 🚫
"""

user_stats = """
<b>📊 Статистика пользователя 📊</b>
"""

categories = """
<b>📜 Список категорий слов 🏷:</b>
"""

true_answer = """
Правильно 🎯, молодец! 🥳 
"""

false_answer = """
К сожалению, вы ошиблись 😔. Попробуйте снова 🤓
"""

repeat = f"""
Вы уже отгадали это слово 🤔. Нажмите {KEYBOARD['NEXT_STEP']}
"""

wrong_format = f"""
Неверный формат слова 📝 :( Попробуйте снова 🤓
"""

wrong_cat_format = f"""
Неверный формат категории 🏷 :( Попробуйте снова 🤓
"""

enter_word = f"""
Введите 👉 слово 📝 на русском 🇷🇺 или на английском 🇺🇸
"""

enter_category = f"""
Введите 👉 категорию 🏷 (<i>all</i> или <i>все</i> - <i>Общая</i> категория):
"""

next_word = """
Что в переводе означает слово: 
"""

add_word_eng = """
Введите 👉 слово на английском языке 🇺🇸
"""

add_word_rus = """
Введите 👉 слово на русском языке 🇷🇺
"""

add_category = """
Введите 👉 категорию для нового слова 🏷:
"""

bot_description = f"""
Бот для изучения английского языка. 
Бот поможет вам изучить английский язык по карточкам. 
Версия бота: {settings.VERSION}
Автор: {settings.AUTHOR}{KEYBOARD['COPY']}
"""

MESSAGES = {
    'BOT_DESCRIPTION': bot_description,
    'HELP': help,
    'START': start,
    'LETS_START': lets_start,
    'END_ROUND': end_round,
    'ROUND_RESULTS': round_results,
    'NOTIF_ON': notification_on,
    'NOTIF_OFF': notification_off,
    'ENG_TO_RUS': eng_to_rus,
    'RUS_TO_ENG': rus_to_eng,
    'USER_STATS': user_stats,
    'CATEGORIES': categories,
    'TRUE_ANSWER': true_answer,
    'FALSE_ANSWER': false_answer,
    'REPEAT': repeat,
    'WORDS_AMOUNT': words_amount,
    'CHANGE_WORDS_AMOUNT': change_words_amount,
    'WRONG_AMOUNT': wrong_amount,
    'RESET_SUCCESS': reset_success,
    'RESET_FAILED': reset_failed,
    'HINT': hint,
    'NO_HINT': no_hint,
    'WELCOME': welcome,
    'WELCOME_BACK': welcome_back,
    'NEXT_WORD': next_word,
    'INFO': info,
    'ADD_WORD_ENG': add_word_eng,
    'ADD_WORD_RUS': add_word_rus,
    'ADD_CATEGORY': add_category,
    'WRONG_FORMAT': wrong_format,
    'WRONG_CAT_FORMAT': wrong_cat_format,
    'ENTER_WORD': enter_word,
    'ENTER_CATEGORY': enter_category
}
