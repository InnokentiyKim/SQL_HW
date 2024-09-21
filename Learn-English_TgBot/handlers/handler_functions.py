from handlers.handler_core import Handler
from telebot.types import Message
from models.bot_user import BotUser
from models.user_settings import UserSettings
from settings.config import KEYBOARD, TranslationMode, ALIASES, SETTINGS_KEYBOARD, NAVIGATION_KEYBOARD
from settings.messages import MESSAGES
from play_session.session_main import PlaySession


class HandlerFunctions(Handler):
    def __init__(self, bot):
        super().__init__(bot)
        self.play_session = PlaySession()
        self.new_users_word = {}

    def get_help(self, message):
        self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['HELP']}", parse_mode='html')

    def start_actions(self, message):
        user_id = int(message.from_user.id)
        user_name = message.from_user.first_name
        user = self.DB.identify_user(user_id)
        if not user:
            user = self.DB.add_new_user(user_id, user_name)
            self.bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Будем знакомы!")
            self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['START']}")
        else:
            self.bot.send_message(message.chat.id, f"С возвращением, {message.from_user.first_name}! Рада видеть вас снова!")
        self.play_session.init_session(user)
        self.bot.send_message(message.chat.id, f"Чтобы начать введите команду '/cards'")

    def get_next_card(self, message, play_mode: TranslationMode = TranslationMode.RUS_TO_ENG):
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
            main_keyboard = self.markup.get_main_keyboard(word_names, NAVIGATION_KEYBOARD)
            self.markup.active_keyboard = main_keyboard
            self.bot.send_message(message.chat.id, f"{words_message} {target_title}", reply_markup=main_keyboard)
        else:
            user = self.play_session.user
            if not user:
                user = self.DB.identify_user(message.from_user.id)
            self.play_session.init_session(user)
            self.bot.send_message(message.chat.id, f"Список слов закончился. Нажмите далее для загрузки следующего списка",
                                  reply_markup=self.markup.active_keyboard)


    def get_hint(self, message, word: str = None) -> None:
        # TODO: implement in-memory cached hints
        word = self.play_session.current_target_word.eng_title if not word else word.lower().strip()
        hint = self.play_session.get_words_description(word)
        if hint:
            self.bot.send_message(message.chat.id, f"Подсказка: {hint}")
        else:
            self.bot.send_message(message.chat.id, f"К сожалению, подсказка недоступна")

    # def get_bots_menu(self, message, menu_list: list[str] | None = None, one_time: bool = False):
    #     if not menu_list:
    #         menu_list = [KEYBOARD['INFO'], KEYBOARD['SETTINGS'], KEYBOARD['HELP']]
    #     menu_keyboard = self.markup.get_menu_keyboard(menu_list, one_time=one_time)
    #     self.bot.send_message(message.chat.id, f"Вы вошли в МЕНЮ", reply_markup=menu_keyboard)
    #     return menu_keyboard

    def add_new_word(self, message, rus_title: str, eng_title: str, category_name: str):
        user = self.play_session.user
        category_name = category_name.lower().strip()
        if category_name in ALIASES.get('BASIC'):
            is_word_added = self.DB.add_new_word(user=user, rus_title=rus_title, eng_title=eng_title)
        else:
            is_word_added = self.DB.add_new_word(user=user, rus_title=rus_title,
                                             eng_title=eng_title, category_name=category_name)
        words_title = f"({rus_title} - {eng_title})"
        if is_word_added:
            self.bot.send_message(message.chat.id, f"Слово {words_title} добавлено",
                                  reply_markup=self.markup.active_keyboard, parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, f"Слово {words_title} уже существует",
                                  reply_markup=self.markup.active_keyboard, parse_mode='html')

    def delete_word(self, message, word: str):
        user = self.play_session.user
        word_deleted = self.DB.delete_word(user=user, word=word)
        if word_deleted:
            self.bot.send_message(message.chat.id, f"Слово ({word}) удалено",
                                  reply_markup=self.markup.active_keyboard, parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, f"Слово ({word}) не найдено",
                                  reply_markup=self.markup.active_keyboard, parse_mode='html')

    @staticmethod
    def _suit_user_settings(input_settings: UserSettings) -> str:
        formatted_settings = {}
        if input_settings.translation_mode == TranslationMode.RUS_TO_ENG:
            formatted_settings['Режим перевода'] = 'С русского на английский'
        elif input_settings.translation_mode == TranslationMode.ENG_TO_RUS:
            formatted_settings['Режим перевода'] = 'С английского на русский'
        if input_settings.notification:
            formatted_settings['Уведомления'] = 'Включены'
        else:
            formatted_settings['Уведомления'] = 'Отключены'
        res_string = "; ".join([f"{key}: {value}" for key, value in formatted_settings.items()])
        return res_string

    def get_user_settings(self, message):
        user_settings = self.play_session.user.user_settings
        if user_settings:
            settings_string = self._suit_user_settings(user_settings)
            answer_str = f"Текущие настройки:\n{settings_string}"
        else:
            answer_str = "Не удалось получить настройки"
        settings_keyboard = self.markup.get_settings_keyboard(SETTINGS_KEYBOARD)
        self.bot.send_message(message.chat.id, answer_str,
                              reply_markup=settings_keyboard, parse_mode='html')

    def get_info(self, message):
        main_keyboard = self.markup.active_keyboard
        self.bot.send_message(message.chat.id, MESSAGES['INFO'], reply_markup=main_keyboard, parse_mode='html')

    def get_step_back(self, message):
        main_keyboard = self.markup.active_keyboard
        self.bot.send_message(message.chat.id, f"Вы вернулись назад", reply_markup=main_keyboard, parse_mode='html')

    def check_answer(self, message: Message, play_mode: TranslationMode = TranslationMode.RUS_TO_ENG):
        target_word = self.play_session.current_target_word
        answer = str(message.text).capitalize().strip()
        if not self.play_session.is_answered and target_word:
            true_answer = ''
            if play_mode == TranslationMode.RUS_TO_ENG:
                true_answer = target_word.eng_title
            elif play_mode == TranslationMode.ENG_TO_RUS:
                true_answer = target_word.rus_title
            if true_answer.capitalize().strip() == answer:
                self.play_session.increase_target_words_stats()
                self.play_session.increase_player_stats()
                self.bot.send_message(message.chat.id, "Правильно", reply_markup=self.markup.active_keyboard)
            else:
                self.play_session.decrease_target_words_stats()
                self.play_session.decrease_player_stats()
                self.bot.send_message(message.chat.id, "К сожалению, вы ошиблись. Попробуйте снова")
                self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']} "
                                                       f"{target_word.rus_title}", reply_markup=self.markup.active_keyboard)
        else:
            self.bot.send_message(message.chat.id, "Вы уже отгадали это слово. Нажмите 'Далее'",
                                  reply_markup=self.markup.active_keyboard)

    @staticmethod
    def validate_input_word(word: str) -> bool:
        # TODO: add validation using regex
        if isinstance(word, str):
            if word.strip() and '.,!?-;' not in word:
                return True
        return False

    def handle(self):
        pass

