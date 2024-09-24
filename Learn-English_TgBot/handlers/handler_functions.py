import re
from datetime import datetime, UTC
from random import shuffle

from bot_logging.bot_logging import LOGGER_PATH, error_logging
from handlers.handler_core import Handler
from telebot.types import Message
from models.bot_user import BotUser
from models.user_settings import UserSettings
from settings.config import KEYBOARD, TranslationMode, ALIASES, SETTINGS_KEYBOARD, NAVIGATION_KEYBOARD, settings, \
    CATEGORIES
from settings.messages import MESSAGES
from play_session.session_main import PlaySession


class HandlerFunctions(Handler):
    """
    Класс функций обработчика. Предоставляет методы для обработчика событий.
    Расширяет класс Handler и предоставляет методы для обработки различных функций.
    Обеспечивает взаимодействие с базой данных и другими компонентами системы.
    Атрибуты:
        play_session: Объект сессии игры
        new_users_word: Слово для нового пользователя
    Методы:
        get_help - Отправляет сообщение для помощи пользователю
        start_actions - Инициализирует сессию игры и выполняет начальные действия
        update_users_play_stats - Обновляет в базе данных статистику пользователя
        get_next_card - Получает следующую карточку со словами
        change_notification_state - Изменяет состояние уведомлений
        change_translation_mode - Изменяет режим перевода
        change_words_chunk_size - Изменяет размер блока слов раунда игры
        reset_all_settings - Сбрасывает все настройки пользователя до стандартных значений
        get_hint - Отправляет пользователю подсказку
        add_new_word - Добавляет новое слово в базу данных
        delete_word - Удаляет слово из базы данных
        get_user_settings - Отправляет пользователю его текущие настройки
        get_info - Отправляет пользователю информацию о боте
        show_user_statistics - Отправляет пользователю его статистику
        check_answer - Проверяет правильность ответа пользователя
        validate_input_word - Валидирует введенное пользователем слово
        validate_input_number - Валидирует введенное пользователем число
    """
    def __init__(self, bot):
        super().__init__(bot)
        self.play_session = PlaySession()
        self.new_users_word = {}

    def get_help(self, message):
        """
        Возвращает справку по командам.
        Обрабатывает команду /help и возвращает список доступных команд с их описанием.
        Параметры:
            message: Объект сообщения от пользователя.
            """
        self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['HELP']}", parse_mode='html')

    def start_actions(self, message):
        """
        Выполняет начальные действия при запуске бота, включая добавление нового пользователя и инициализацию сессии.
        Обрабатывает команду /start и выполняет необходимые действия при запуске бота,
        такие как приветствие пользователя и отправка клавиатуры управления.
        Параметры:
            message: Объект сообщения от пользователя.
        Возвращает:
            None
        """
        user_id = int(message.from_user.id)
        user_name = message.from_user.first_name
        user = self.DB.identify_user(user_id)
        if not user:
            user = self.DB.add_new_user(user_id, user_name)
            self.bot.send_message(message.chat.id, f"{message.from_user.first_name}{MESSAGES['WELCOME']}")
            self.bot.send_message(message.chat.id, f"{message.from_user.first_name}{MESSAGES['START']}")
        else:
            self.bot.send_message(message.chat.id, f"{message.from_user.first_name}{MESSAGES['WELCOME_BACK']}")
        self.play_session.init_session(bot_user=user, words_category=CATEGORIES['COMMON']['name'],
                                       words_amount=user.user_settings.words_chunk_size)
        self.bot.send_message(message.chat.id, f"{MESSAGES['LETS_START']}", parse_mode='html')

    def update_users_play_stats(self) -> bool:
        """
       Обновляет статистику игровой активности пользователя в базе данных.
       Также обновляет статистику слов пользователя в базе данных.
       Возвращает:
           bool - True, если обновление прошло успешно, иначе False
       """
        self.play_session.user.last_seen_at = datetime.now(tz=UTC)
        updating_status = self.DB.update_users_stats(self.play_session.user, self.play_session.target_words)
        return updating_status

    @error_logging(LOGGER_PATH)
    def get_next_card(self, message, play_mode: TranslationMode = TranslationMode.RUS_TO_ENG):
        """
        Возвращает следующую карточку слов для пользователя.
        Выбирает следующую карточку для пользователя в зависимости от режима перевода из указанной категории.
        Если карточки в текущей сессии закончились, то выводит результаты раунда, обновляет статистику пользователя
        в базе данных и инициализирует новую сессию.
        Параметры:
            message: Объект сообщения от пользователя.
            play_mode (TranslationMode): Режим перевода.
        Возвращает:
            None
        """
        card = self.play_session.get_words_for_card()
        if card:
            word_names = []
            words_message = ''
            target_title = ''
            if play_mode == TranslationMode.RUS_TO_ENG:
                word_names = [word.eng_title for word in card.get('all')]
                target_title = card.get('target').rus_title
                words_message = f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']}"
            elif play_mode == TranslationMode.ENG_TO_RUS:
                word_names = [word.rus_title for word in card.get('all')]
                target_title = card.get('target').eng_title
                words_message = f"{MESSAGES['NEXT_WORD']} {KEYBOARD['ENG']}"
            shuffle(word_names)
            main_keyboard = self.markup.get_main_keyboard(word_names, NAVIGATION_KEYBOARD)
            self.markup.active_keyboard = main_keyboard
            self.bot.send_message(message.chat.id, f"{words_message} {target_title}", reply_markup=main_keyboard)
        else:
            user = self.play_session.user
            if not user:
                user = self.DB.identify_user(message.from_user.id)
            round_stats_str = (f"<i>Количество попыток: {self.play_session.round_attempts}</i>\n"
                               f"<i>Правильных ответов: {self.play_session.round_successful_attempts}</i>")
            self.update_users_play_stats()
            self.play_session.init_session(bot_user=user, words_category=CATEGORIES['COMMON']['name'], words_amount=user.user_settings.words_chunk_size)
            self.bot.send_message(message.chat.id, MESSAGES['END_ROUND'], parse_mode='html')
            self.bot.send_message(message.chat.id, f"{MESSAGES['ROUND_RESULTS']}\n{round_stats_str}",
                                  reply_markup=self.markup.active_keyboard, parse_mode='html')

    def change_notification_state(self, call):
        """
        Изменяет состояние уведомлений для пользователя (включено/выключено).
        Параметры:
            call: Объект CallbackQuery от пользователя.
        Возвращает:
            None
        """
        user_settings = self.play_session.user.user_settings
        if user_settings.notification == 0:
            user_settings.notification = 1
        else:
            user_settings.notification = 0
        self.DB.update_user_settings(self.play_session.user)
        answer = MESSAGES['NOTIF_ON'] if not user_settings.notification else MESSAGES['NOTIF_OFF']
        self.bot.send_message(chat_id=call.message.chat.id, text=answer)

    def change_translation_mode(self, call):
        """
        Изменяет режим перевода для пользователя ("en-ru"/"ru-en").
        Параметры:
            call: Объект CallbackQuery от пользователя.
        Возвращает:
            None
        """
        user_settings = self.play_session.user.user_settings
        if user_settings.translation_mode == TranslationMode.ENG_TO_RUS:
            user_settings.translation_mode = TranslationMode.RUS_TO_ENG
        elif user_settings.translation_mode == TranslationMode.RUS_TO_ENG:
            user_settings.translation_mode = TranslationMode.ENG_TO_RUS
        self.DB.update_user_settings(self.play_session.user)
        answer = MESSAGES['ENG_TO_RUS'] if user_settings.translation_mode == TranslationMode.ENG_TO_RUS \
            else MESSAGES['RUS_TO_ENG']
        self.bot.send_message(chat_id=call.message.chat.id, text=answer)

    def change_words_chunk_size(self, message):
        """
        Изменяет количество слов в раунде для пользователя.
        Также выполняет валидацию введенного пользователем числа.
        Параметры:
            message (Message): Объект сообщения от пользователя.
        Возвращает:
            None
        """
        user_settings = self.play_session.user.user_settings
        input_number = self.validate_input_number(message.text, settings.MIN_WORDS_CHUNK_SIZE, settings.OTHER_WORDS_CHUNK_SIZE)
        if input_number:
            user_settings.words_chunk_size = input_number
            self.DB.update_user_settings(self.play_session.user)
        answer = f"{MESSAGES['CHANGE_WORDS_AMOUNT']} {input_number}" if input_number else MESSAGES['WRONG_AMOUNT']
        self.bot.send_message(chat_id=message.chat.id, text=answer, reply_markup=self.markup.active_keyboard)

    def reset_all_settings(self, call) -> None:
        """
        Сбрасывает все настройки пользователя до значений по умолчанию.
        Параметры:
            call (CallbackQuery): Объект CallbackQuery от пользователя.
        Возвращает:
            None
        """
        user_settings = self.play_session.user.user_settings
        user_settings.words_chunk_size = settings.TARGET_WORDS_CHUNK_SIZE
        user_settings.translation_mode = TranslationMode.RUS_TO_ENG
        user_settings.notification = 0
        answer = MESSAGES['RESET_FAILED']
        if self.DB.update_user_settings(self.play_session.user):
            answer = MESSAGES['RESET_SUCCESS']
        self.bot.send_message(call.message.chat.id, answer, parse_mode='html')

    def get_hint(self, message, word: str = None) -> None:
        """
        Отправляет пользователю подсказку для загаданного слова.
        Использует внешний API для получения подсказки.
        Параметры:
            message (Message): Объект сообщения от пользователя.
            word (str): Загаданное слово.
        Возвращает:
            None
        """
        word = self.play_session.current_target_word.eng_title if not word else word.lower().strip()
        hint = self.play_session.get_words_description(word)
        if hint:
            self.bot.send_message(message.chat.id, f"{MESSAGES['HINT']} <i>{hint}</i>", parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, MESSAGES['NO_HINT'], parse_mode='html')

    def add_new_word(self, message, rus_title: str, eng_title: str, category_name: str):
        """
        Добавляет новое слово пользователя в базу данных в указанную категорию.
        Новое слово в любом случае добавляется в категорию "Общие".
        Отправляет пользователю сообщение об успешном или неуспешном добавлении.
        Параметры:
            message (Message): Объект сообщения от пользователя.
            rus_title (str): Русское название слова.
            eng_title (str): Английское название слова.
            category_name (str): Название категории.
        Возвращает:
            None
        """
        user = self.play_session.user
        category_name = category_name.lower().strip()
        if category_name in ALIASES.get('BASIC'):
            is_word_added = self.DB.add_new_word(user=user, rus_title=rus_title, eng_title=eng_title)
        else:
            is_word_added = self.DB.add_new_word(user=user, rus_title=rus_title,
                                             eng_title=eng_title, category_name=category_name)
        words_title = f"<b><i>{rus_title} - {eng_title}</i></b>"
        category_title = f"<b><i>{category_name}</i></b>"
        if is_word_added:
            self.bot.send_message(message.chat.id, f"Слово {words_title} добавлено в категорию {category_title}",
                                  reply_markup=self.markup.active_keyboard, parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, f"Слово {words_title} уже существует",
                                  reply_markup=self.markup.active_keyboard, parse_mode='html')

    def delete_word(self, message, word: str):
        """
        Удаляет слово из базы данных по названию (английскому или русскому).
        Удаляет слово и все связанные с ним данные.
        Отправляет пользователю сообщение об успешном или неуспешном удалении.
        Параметры:
            message (Message): Объект сообщения от пользователя.
            word (str): Название слова.
        Возвращает:
            None
        """
        user = self.play_session.user
        word_deleted = self.DB.delete_word(user=user, word=word)
        if word_deleted:
            self.bot.send_message(message.chat.id, f"Слово <b><i>{word}</i></b> удалено",
                                  reply_markup=self.markup.active_keyboard, parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, f"Слово <b><i>{word}</i></b> не найдено",
                                  reply_markup=self.markup.active_keyboard, parse_mode='html')

    @staticmethod
    def _suit_user_settings(input_settings: UserSettings) -> str:
        res_string = f"<b>Текущие настройки:</b>\n\n"
        formatted_settings = {}
        formatted_settings['Количество слов в раунде'] = input_settings.words_chunk_size
        if input_settings.translation_mode == TranslationMode.RUS_TO_ENG:
            formatted_settings['Режим перевода'] = MESSAGES['RUS_TO_ENG']
        elif input_settings.translation_mode == TranslationMode.ENG_TO_RUS:
            formatted_settings['Режим перевода'] = MESSAGES['ENG_TO_RUS']
        if input_settings.notification:
            formatted_settings['Напоминания'] = MESSAGES['NOTIF_ON']
        else:
            formatted_settings['Напоминания'] = MESSAGES['NOTIF_OFF']
        res_string = res_string + "\n".join([f"<b><i>{key}</i></b>: <i>{value}</i>" for key, value in formatted_settings.items()])
        return res_string

    def get_user_settings(self, message):
        """
        Возвращает настройки пользователя.
        Отправляет пользователю сообщение с текущими настройками.
        Параметры:
            message (Message): Объект сообщения от пользователя.
        Возвращает:
            None
        """
        user_settings = self.play_session.user.user_settings
        if user_settings:
            answer_str = self._suit_user_settings(user_settings)
        else:
            answer_str = "<b>Не удалось получить настройки</b>"
        settings_keyboard = self.markup.get_settings_keyboard(SETTINGS_KEYBOARD)
        self.bot.send_message(message.chat.id, answer_str,
                              reply_markup=settings_keyboard, parse_mode='html')

    @error_logging(LOGGER_PATH)
    def get_info(self, message):
        """
        Отправляет пользователю информацию о боте.
        Параметры:
            message (Message): Объект сообщения от пользователя.
        Возвращает:
            None
        """
        main_keyboard = self.markup.active_keyboard
        self.bot.send_message(message.chat.id, MESSAGES['INFO'], reply_markup=main_keyboard, parse_mode='html')

    @staticmethod
    def _suit_user_stats(user: BotUser, categories: list[str], words_in_study: int) -> str:
        user_stats_str = f"{MESSAGES['USER_STATS']}\n"
        category_stats_str = f"{MESSAGES['CATEGORIES']}\n"
        user_stats = user.user_stats
        rating = user_stats.successful_attempts / user_stats.number_of_attempts * 100 if user_stats.number_of_attempts > 0 else 0
        stats = {'Всего попыток': f'{user_stats.number_of_attempts}', 'Успешных попыток': f'{user_stats.successful_attempts}',
                 'Рейтинг': f'{rating:.1f}%', 'Слов в изучении': f'{words_in_study}'}
        user_stats_str = user_stats_str + "\n".join([f"<b>{key}</b>: <i>{value}</i>" for key, value in stats.items()])
        category_stats_str = category_stats_str + "\t".join([f"<i>{category}</i>" for category in categories])
        suited_str = user_stats_str + "\n" + category_stats_str
        return suited_str

    def show_user_statistics(self, message):
        """
        Получает статистику пользователя, включая категории, количество изучаемых слов, правильных ответов и т.д.
        Отправляет пользователю статистику.
        Параметры:
            message (Message): Объект сообщения от пользователя.
        Возвращает:
            None
        """
        user = self.play_session.user
        category_objects = self.DB.get_all_users_categories(user.id)
        categories_list = [category.name for category in category_objects]
        words_in_study = self.DB.get_studying_words_count(user.id)
        answer_str = self._suit_user_stats(user, categories_list, words_in_study)
        self.bot.send_message(message.chat.id, answer_str, reply_markup=self.markup.active_keyboard, parse_mode='html')

    @error_logging(LOGGER_PATH)
    def check_answer(self, message: Message, play_mode: TranslationMode = TranslationMode.RUS_TO_ENG):
        """
        Проверяет ответ пользователя на загаданное слово с учетом текущего режима перевода.
        Отправляет пользователю результат проверки.
        Параметры:
            message (Message): Объект сообщения от пользователя.
            play_mode (TranslationMode): Режим перевода.
        Возвращает:
            None
        """
        target_word = self.play_session.current_target_word
        question = target_word.eng_title
        answer = str(message.text).capitalize().strip()
        if not self.play_session.is_answered and target_word:
            true_answer = ''
            if play_mode == TranslationMode.RUS_TO_ENG:
                true_answer = target_word.eng_title
                question = f"{KEYBOARD['RUS']} {target_word.rus_title}"
            elif play_mode == TranslationMode.ENG_TO_RUS:
                true_answer = target_word.rus_title
                question = f"{KEYBOARD['ENG']} {target_word.eng_title}"
            if true_answer.capitalize().strip() == answer:
                self.play_session.increase_target_words_stats()
                self.play_session.increase_player_stats()
                self.bot.send_message(message.chat.id, MESSAGES['TRUE_ANSWER'],
                                      reply_markup=self.markup.active_keyboard, parse_mode='html')
            else:
                self.play_session.decrease_target_words_stats()
                self.play_session.decrease_player_stats()
                self.bot.send_message(message.chat.id, MESSAGES['FALSE_ANSWER'], parse_mode='html')
                self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {question} ",
                                      reply_markup=self.markup.active_keyboard, parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, MESSAGES['REPEAT'],
                                  reply_markup=self.markup.active_keyboard, parse_mode='html')

    @staticmethod
    @error_logging(LOGGER_PATH)
    def validate_input_word(word: str, language: str = 'all') -> bool:
        """
        Проводит валидацию слов на основе регулярных выражений с учетом языка.
        Параметры:
            word (str): Слово для валидации.
            language (str): Язык проверки.
        Возвращает:
            bool: True, если слово корректно, False в противном случае.
        """
        word_pattern = r'^[a-zA-Zа-яА-ЯёЁ-]+'
        if language == 'eng':
            word_pattern = r'^[a-zA-Z-]+'
        elif language == 'rus':
            word_pattern = r'^[а-яА-ЯёЁ-]+'
        if isinstance(word, str):
            if re.fullmatch(word_pattern, word):
                return True
        return False

    @staticmethod
    @error_logging(LOGGER_PATH)
    def validate_input_number(number: str, min_value: int, max_value: int) -> int:
        """
        Проводит валидацию введенного пользователем числа на основе регулярных выражений.
        Параметры:
            number (str): Число для валидации.
            min_value (int): Минимальное значение.
            max_value (int): Максимальное значение.
        Возвращает:
            int: Число, если оно корректно, 0 в противном случае.
        """
        if isinstance(number, str):
            if number.isdigit() and min_value <= int(number) < max_value:
                return int(number)
            return 0

    def handle(self):
        pass

