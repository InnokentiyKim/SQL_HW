from handlers.handler import Handler
from settings.config import COMMANDS, KEYBOARD, USER_STATES
from settings.message import MESSAGES
import telebot.types as tbtypes


class HandlerMain(Handler):
    def __init__(self, bot):
        super().__init__(bot)
        self.current_state = USER_STATES['PLAYING']
        self.current_message = None

    def pressed_button_help(self, message):
        self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['HELP']}", parse_mode='html')

    def pressed_button_start(self, message):
        self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['START']}")

    def pressed_button_cards(self, message):
        user_id = int(message.from_user.id)
        user_name = message.from_user.first_name
        if not self.DB.identified_user(user_id):
            self.DB.init_default_cards(user_id)
        main_keyboard = self.keyboards.get_next_word_keyboard(user_id)
        self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']} "
                                               f"{self.DB.target_word.rus_title}", reply_markup=main_keyboard)

    def pressed_button_menu(self, message):
        menu_keyboard = self.keyboards.get_menu_keyboard()
        self.bot.send_message(message.chat.id, f"{KEYBOARD['MENU']}", reply_markup=menu_keyboard)
        return menu_keyboard

    def _get_new_rus_word(self, message):
        self.current_message = message
        self.pressed_button_add_word(message)
        return message

    def _change_state(self, state):
        self.current_state = state

    def pressed_button_add_word(self, message):
        user_id = int(message.from_user.id)
        word_rus_title = "Мое новое слово"
        word_eng_title = "My new word"
        word_category = "My new category"
        word_added = self.DB.add_word(user_id, word_rus_title, word_eng_title)
        if word_added:
            self.bot.send_message(message.chat.id, f"Слово {word_rus_title} - {word_eng_title} добавлено",
                                  reply_markup=self.keyboards.active_keyboard)
        else:
            self.bot.send_message(message.chat.id, f"Слово {word_rus_title} - {word_eng_title} уже существует",
                                  reply_markup=self.keyboards.active_keyboard)
        # self.bot.send_message(message.chat.id, f"{MESSAGES['ADD_WORD_RUS']}")
        # word_rus_title = self.current_message.text
        # self.bot.send_message(self.current_message.chat.id, f"{MESSAGES['ADD_WORD_ENG']}")
        # word_eng_title = self.current_message.text
        # self.bot.send_message(self.current_message.chat.id, f"{MESSAGES['ADD_CATEGORY']}")
        # words_category = self.current_message.text
        # word_added = self.DB.add_word(user_id, word_rus_title, word_eng_title, words_category)
        # if word_added:
        #     self.bot.send_message(message.chat.id, f"Слово {word_rus_title} - {word_eng_title} добавлено")
        # else:
        #     self.bot.send_message(message.chat.id, f"Слово {word_rus_title} - {word_eng_title} уже существует")
        # self.current_state = USER_STATES['PLAYING']
        # main_keyboard = self.keyboards.active_keyboard
        # self.bot.send_message(message.chat.id, f"{KEYBOARD['MENU']}", reply_markup=main_keyboard)

    def pressed_button_delete_word(self, message):
        user_id = int(message.from_user.id)
        word = "lion"
        word_deleted = self.DB.delete_word(user_id, word)
        if word_deleted:
            self.bot.send_message(message.chat.id, f"Слово {word} удалено",
                                  reply_markup=self.keyboards.active_keyboard)
        else:
            self.bot.send_message(message.chat.id, f"Слово {word} не существует",
                                  reply_markup=self.keyboards.active_keyboard)

    def pressed_button_settings(self, message):
        pass

    def pressed_button_info(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['INFO'], parse_mode='html')

    def pressed_button_back(self, message):
        main_keyboard = self.keyboards.active_keyboard
        self.bot.send_message(message.chat.id, f"{KEYBOARD['BACK']}", reply_markup=main_keyboard)

    def pressed_button_next(self, message):
        user_id = int(message.from_user.id)
        main_keyboard = self.keyboards.get_next_word_keyboard(user_id)
        self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']} "
                                               f"{self.DB.target_word.rus_title}", reply_markup=main_keyboard)

    def check_answer(self, message):
        answer = str(message.text).lower()
        if self.DB.target_word.eng_title == answer:
            self.bot.send_message(message.chat.id, "Правильно", reply_markup=self.keyboards.active_keyboard)
        else:
            self.bot.send_message(message.chat.id, "К сожалению, вы ошиблись. Попробуйте снова",
                                  reply_markup=self.keyboards.active_keyboard)

    def handle(self):
        @self.bot.message_handler(commands=[COMMANDS['HELP']])
        def handle(message):
            if message.text == '/help':
                self.pressed_button_help(message)

        @self.bot.message_handler(commands=[COMMANDS['START']])
        def handle(message):
            if message.text == '/start':
                self.pressed_button_start(message)

        @self.bot.message_handler(commands=[COMMANDS['CARDS']])
        def handle(message):
            if message.text == '/cards':
                self.pressed_button_cards(message)

        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            chat_id = message.chat.id
            if chat_id not in self.DB.user_states:
                self.DB.user_states[chat_id] = USER_STATES['START']
            if self.DB.user_states[chat_id] == USER_STATES['START']:
                if message.text == KEYBOARD['NEXT_STEP']:
                    self.DB.user_states[chat_id] = USER_STATES['PLAYING']
                    self.pressed_button_next(message)
                elif message.text == KEYBOARD['MENU']:
                    self.DB.user_states[chat_id] = USER_STATES['START']
                    self.pressed_button_menu(message)
                elif message.text == KEYBOARD['BACK']:
                    self.DB.user_states[chat_id] = USER_STATES['PLAYING']
                    self.pressed_button_back(message)
                elif message.text == KEYBOARD['ADD_WORD']:
                    self.current_state = USER_STATES['ADDING_DATA']
                elif message.text == KEYBOARD['DELETE_WORD']:
                    self.current_state = USER_STATES['DELETING_DATA']
                elif message.text == KEYBOARD['SETTINGS']:
                    self.pressed_button_settings(message)
                elif message.text == KEYBOARD['INFO']:
                    self.pressed_button_info(message)
                else:
                    self.check_answer(message)
            elif self.DB.user_states[chat_id] == USER_STATES['ADDING_DATA']:
                self.pressed_button_add_word(message)
                self.DB.user_states[chat_id] = USER_STATES['START']
            elif self.DB.user_states[chat_id] == USER_STATES['DELETING_DATA']:
                self.pressed_button_delete_word(message)
                self.DB.user_states[chat_id] = USER_STATES['START']
