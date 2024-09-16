from handlers.handler_core import Handler
from markup.markups import Markup
from models.bot_user import BotUser
from settings.config import KEYBOARD, TranslationMode
from settings.messages import MESSAGES
from settings.config import settings
from play_session.session_main import PlaySession
import requests


class HandlerFunctions(Handler):
    def __init__(self, bot):
        super().__init__(bot)
        self.play_session = PlaySession()

    def get_help(self, message):
        self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['HELP']}", parse_mode='html')

    def start_actions(self, message):
        user = self.DB.identify_user(message.from_user.id)
        if not user:
            user = self.DB.add_new_user(message.from_user.id, message.from_user.first_name)
        self.play_session.init_session(user)
        self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['START']}")

    def get_next_card(self, message, play_mode: TranslationMode):
        card = self.play_session.get_words_for_card()
        navigation_names = [KEYBOARD['INFO'], KEYBOARD['NEXT_STEP']]
        if card:
            if play_mode == TranslationMode.RUS_TO_ENG:
                button_names = [word.eng_title for word in card.get('all')]
                main_keyboard = self.markup.get_main_keyboard(button_names, navigation_names)
                self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']} "
                                                       f"{card.get('target').rus_title}", reply_markup=main_keyboard)
            elif play_mode == TranslationMode.ENG_TO_RUS:
                button_names = [word.rus_title for word in card.get('all')]
                main_keyboard = self.markup.get_main_keyboard(button_names, navigation_names)
                self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['ENG']}"
                                                       f"{card.get('target').eng_title}", reply_markup=main_keyboard)
        else:
            pass

    @staticmethod
    def get_words_description(word: str) -> dict:
        try:
            response = requests.get(settings.WORDS_URL, params={'words': word}).json()
            description = response.get('description')
        except Exception as error:
            description = None
        return description

    def get_bots_menu(self, message, menu_list: list[str] | None = None, one_time: bool = False):
        if not menu_list:
            menu_list = [KEYBOARD['INFO'], KEYBOARD['SETTINGS'], KEYBOARD['HELP']]
        menu_keyboard = self.markup.get_menu_keyboard(menu_list, one_time=one_time)
        self.bot.send_message(message.chat.id, f"Вы вошли в МЕНЮ", reply_markup=menu_keyboard)
        return menu_keyboard

    def add_new_word(self, message, rus_word, eng_word, category):
        user_id = int(message.from_user.id)
        word_rus_title = rus_word
        word_eng_title = eng_word
        word_category = category
        word_added = self.DB.add_word(user_id, word_rus_title, word_eng_title, word_category)
        menu_keyboard = self.markup.get_menu_keyboard()
        if word_added:
            self.bot.send_message(message.chat.id, f"Слово {word_rus_title} - {word_eng_title} добавлено",
                                  reply_markup=menu_keyboard, parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, f"Слово {word_rus_title} - {word_eng_title} уже существует",
                                  reply_markup=menu_keyboard, parse_mode='html')

    def delete_word(self, message, word):
        user_id = int(message.from_user.id)
        word_deleted = self.DB.delete_word(user_id, word)
        menu_keyboard = self.markup.get_menu_keyboard()
        if word_deleted:
            self.bot.send_message(message.chat.id, f"Слово {word} удалено",
                                  reply_markup=menu_keyboard, parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, f"Слово {word} не существует",
                                  reply_markup=menu_keyboard, parse_mode='html')

    def get_user_settings(self, message):
        pass

    def get_info(self, message):
        menu_keyboard = self.markup.get_menu_markup()
        self.bot.send_message(message.chat.id, MESSAGES['INFO'], reply_markup=menu_keyboard, parse_mode='html')

    def get_step_back(self, message):
        main_keyboard = self.markup.active_keyboard
        self.bot.send_message(message.chat.id, f"Вы вернулись назад", reply_markup=main_keyboard, parse_mode='html')

    def get_step_next(self, message):
        user_id = int(message.from_user.id)
        main_keyboard = self.markup.get_next_word_keyboard(user_id)
        self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']} "
                                               f"{self.DB.target_word.rus_title}", reply_markup=main_keyboard)

    def check_answer(self, message):
        if not self.DB.is_answered:
            answer = str(message.text).capitalize().strip()
            if self.DB.target_word.eng_title == answer:
                self.DB.is_answered = True
                self.bot.send_message(message.chat.id, "Правильно", reply_markup=self.markup.active_keyboard)
                print(self.get_words_description(self.DB.target_word.eng_title))
            else:
                self.bot.send_message(message.chat.id, "К сожалению, вы ошиблись. Попробуйте снова")
                self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']}"
                                                       f"{self.DB.target_word.rus_title}",
                                      reply_markup=self.markup.active_keyboard)
        else:
            self.bot.send_message(message.chat.id, "Вы уже отгадали это слово. Нажмите 'Далее'",
                                  reply_markup=self.markup.active_keyboard)

    def handle(self):
        pass
