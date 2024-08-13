from handlers.handler import Handler
from settings.config import COMMANDS, KEYBOARD, USER_STATES
from settings.messages import MESSAGES
from transitions import Machine
import requests

class WordCardsBot:
    states = ['start', 'playing', 'adding_data', 'deleting_data']
    transitions = [
        {'trigger': 'start', 'source': 'start', 'dest': 'playing'},
        {'trigger': 'playing', 'source': 'playing', 'dest': 'adding_data'},
        {'trigger': 'adding_data', 'source': 'adding_data', 'dest': 'playing'},
        {'trigger': 'deleting_data', 'source': 'deleting_data', 'dest': 'playing'},
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=WordCardsBot.states, transitions=WordCardsBot.transitions, initial='start')


class HandlerMain(Handler):
    def __init__(self, bot):
        super().__init__(bot)
        self.current_state = USER_STATES['PLAYING']
        self.current_message = None
        self.users = {}
        self.words_desription = []
        self.base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

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
    def _generate_url(self, base_url, word):
        return f"{base_url}{word}"

    def get_words_description(self, word):
        url = self._generate_url(self.base_url, word)
        response = requests.get(url).json()
        return response

    def pressed_button_menu(self, message):
        menu_keyboard = self.keyboards.get_menu_keyboard()
        self.bot.send_message(message.chat.id, f"Вы вошли в МЕНЮ", reply_markup=menu_keyboard)
        return menu_keyboard

    def pressed_button_add_word(self, message, rus_word, eng_word, category):
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

    def pressed_button_delete_word(self, message, word):
        user_id = int(message.from_user.id)
        word_deleted = self.DB.delete_word(user_id, word)
        menu_keyboard = self.keyboards.get_menu_keyboard()
        if word_deleted:
            self.bot.send_message(message.chat.id, f"Слово {word} удалено",
                                  reply_markup=menu_keyboard, parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, f"Слово {word} не существует",
                                  reply_markup=menu_keyboard, parse_mode='html')

    def pressed_button_settings(self, message):
        pass

    def pressed_button_info(self, message):
        menu_keyboard = self.keyboards.get_menu_keyboard()
        self.bot.send_message(message.chat.id, MESSAGES['INFO'], reply_markup=menu_keyboard, parse_mode='html')

    def pressed_button_back(self, message):
        main_keyboard = self.keyboards.active_keyboard
        self.bot.send_message(message.chat.id, f"Вы вернулись назад", reply_markup=main_keyboard, parse_mode='html')

    def pressed_button_next(self, message):
        user_id = int(message.from_user.id)
        main_keyboard = self.keyboards.get_next_word_keyboard(user_id)
        self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']} "
                                               f"{self.DB.target_word.rus_title}", reply_markup=main_keyboard)

    def check_answer(self, message):
        if not self.DB.is_answered:
            answer = str(message.text).lower()
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

        @self.bot.message_handler(func=lambda message: message.text == KEYBOARD['ADD_WORD'])
        def handle_new_word(message):
            chat_id = message.chat.id
            self.bot.send_message(chat_id, "Введите слово на русском: ")
            self.users[chat_id] = {}
            self.bot.register_next_step_handler(message, get_rus_word)

        def get_rus_word(message):
            chat_id = message.chat.id
            self.users[chat_id]['rus'] = message.text
            self.bot.send_message(chat_id, "Введите слово на английском: ")
            self.bot.register_next_step_handler(message, get_eng_word)

        def get_eng_word(message):
            chat_id = message.chat.id
            self.users[chat_id]['eng'] = message.text
            self.bot.send_message(chat_id, "Введите категорию: ")
            self.bot.register_next_step_handler(message, get_category)

        def get_category(message):
            chat_id = message.chat.id
            self.users[chat_id]['category'] = message.text
            self.pressed_button_add_word(message, self.users[chat_id]['rus'], self.users[chat_id]['eng'],
                                         self.users[chat_id]['category'])

        @self.bot.message_handler(func=lambda message: message.text == KEYBOARD['DELETE_WORD'])
        def handle_delete_word(message):
            chat_id = message.chat.id
            self.bot.send_message(chat_id, "Введите слово на русском или на английском: ")
            self.users[chat_id] = {}
            self.bot.register_next_step_handler(message, get_deleting_word)

        def get_deleting_word(message):
            chat_id = message.chat.id
            self.users[chat_id]['delete_word'] = message.text
            self.pressed_button_delete_word(message, self.users[chat_id]['delete_word'])

        @self.bot.message_handler(func=lambda message: True)
        def handle_text(message):
            if message.text == KEYBOARD['NEXT_STEP']:
                self.pressed_button_next(message)
            elif message.text == KEYBOARD['MENU']:
                self.pressed_button_menu(message)
            elif message.text == KEYBOARD['BACK']:
                self.pressed_button_back(message)
            elif message.text == KEYBOARD['ADD_WORD']:
                self.step = "add_rus_word"
                self.bot.send_message(message.chat.id, f"Введите слово на русском: ")
            elif message.text == KEYBOARD['DELETE_WORD']:
                self.current_state = USER_STATES['DELETING_DATA']
            elif message.text == KEYBOARD['SETTINGS']:
                self.pressed_button_settings(message)
            elif message.text == KEYBOARD['INFO']:
                self.pressed_button_info(message)
            else:
                self.check_answer(message)
