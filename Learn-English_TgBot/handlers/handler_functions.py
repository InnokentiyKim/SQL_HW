from handlers.handler_core import Handler
from settings.config import KEYBOARD
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
        self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['START']}")

    def get_cards(self, message):
        user_id = int(message.from_user.id)
        # user_name = message.from_user.first_name
        if not self.DB.identified_user(user_id):
            self.DB.init_default_cards(user_id)
        main_keyboard = self.keyboards.get_next_word_keyboard(user_id)
        self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']} "
                                               f"{self.DB.target_word.rus_title}", reply_markup=main_keyboard)

    @staticmethod
    def get_words_description(word: str) -> dict:
        response = requests.get(settings.WORDS_URL, params={'words': word}).json()
        description = response.get('description')
        return description

    def get_bots_menu(self, message):
        menu_keyboard = self.keyboards.get_menu_keyboard()
        self.bot.send_message(message.chat.id, f"Вы вошли в МЕНЮ", reply_markup=menu_keyboard)
        return menu_keyboard

    def add_new_word(self, message, rus_word, eng_word, category):
        user_id = int(message.from_user.id)
        word_rus_title = rus_word
        word_eng_title = eng_word
        word_category = category
        word_added = self.DB.add_word(user_id, word_rus_title, word_eng_title, word_category)
        menu_keyboard = self.keyboards.get_menu_keyboard()
        if word_added:
            self.bot.send_message(message.chat.id, f"Слово {word_rus_title} - {word_eng_title} добавлено",
                                  reply_markup=menu_keyboard, parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, f"Слово {word_rus_title} - {word_eng_title} уже существует",
                                  reply_markup=menu_keyboard, parse_mode='html')

    def delete_word(self, message, word):
        user_id = int(message.from_user.id)
        word_deleted = self.DB.delete_word(user_id, word)
        menu_keyboard = self.keyboards.get_menu_keyboard()
        if word_deleted:
            self.bot.send_message(message.chat.id, f"Слово {word} удалено",
                                  reply_markup=menu_keyboard, parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, f"Слово {word} не существует",
                                  reply_markup=menu_keyboard, parse_mode='html')

    def get_bot_settings(self, message):
        pass

    def get_info(self, message):
        menu_keyboard = self.keyboards.get_menu_keyboard()
        self.bot.send_message(message.chat.id, MESSAGES['INFO'], reply_markup=menu_keyboard, parse_mode='html')

    def get_step_back(self, message):
        main_keyboard = self.keyboards.active_keyboard
        self.bot.send_message(message.chat.id, f"Вы вернулись назад", reply_markup=main_keyboard, parse_mode='html')

    def get_step_next(self, message):
        user_id = int(message.from_user.id)
        main_keyboard = self.keyboards.get_next_word_keyboard(user_id)
        self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']} "
                                               f"{self.DB.target_word.rus_title}", reply_markup=main_keyboard)

    def check_answer(self, message):
        if not self.DB.is_answered:
            answer = str(message.text).capitalize().strip()
            if self.DB.target_word.eng_title == answer:
                self.DB.is_answered = True
                self.bot.send_message(message.chat.id, "Правильно", reply_markup=self.keyboards.active_keyboard)
                print(self.get_words_description(self.DB.target_word.eng_title))
            else:
                self.bot.send_message(message.chat.id, "К сожалению, вы ошиблись. Попробуйте снова")
                self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']}"
                                                       f"{self.DB.target_word.rus_title}",
                                      reply_markup=self.keyboards.active_keyboard)
        else:
            self.bot.send_message(message.chat.id, "Вы уже отгадали это слово. Нажмите 'Далее'",
                                  reply_markup=self.keyboards.active_keyboard)

    def handle(self):
        pass
