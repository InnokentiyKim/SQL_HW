from handlers.handler_core import Handler
from handlers.handler_functions import HandlerFunctions
from settings.config import COMMANDS, KEYBOARD
from settings.messages import MESSAGES
from transitions import Machine


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
        self.handler_functions = HandlerFunctions(bot)
        self.users = {}

    def pressed_button_help(self, message):
        self.handler_functions.get_help(message)

    def pressed_button_start(self, message):
        self.handler_functions.start_actions(message)

    def pressed_button_cards(self, message):
        self.handler_functions.get_cards(message)

    def pressed_button_menu(self, message):
        self.handler_functions.get_bots_menu(message)

    def pressed_button_add_word(self, message, rus_word, eng_word, category):
        self.handler_functions.add_new_word(message, rus_word, eng_word, category)

    def pressed_button_delete_word(self, message, word):
        self.handler_functions.delete_word(message, word)

    def pressed_button_settings(self, message):
        pass

    def pressed_button_info(self, message):
        self.handler_functions.get_info(message)

    def pressed_button_back(self, message):
        self.handler_functions.get_step_back(message)

    def pressed_button_next(self, message):
        self.handler_functions.get_step_next(message)

    def check_answer(self, message):
        if not self.DB.is_answered:
            answer = str(message.text).lower()
            if self.DB.target_word.eng_title == answer:
                self.DB.is_answered = True
                self.bot.send_message(message.chat.id, "Правильно", reply_markup=self.keyboards.active_keyboard)
            else:
                self.bot.send_message(message.chat.id, "К сожалению, вы ошиблись. Попробуйте снова")
                self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']}"
                                                       f"{self.DB.target_word.rus_title}",
                                      reply_markup=self.keyboards.active_keyboard)
        else:
            self.bot.send_message(message.chat.id, "Вы уже отгадали это слово. Нажмите 'Далее'",
                                  reply_markup=self.keyboards.active_keyboard)

    def handle(self):
        @self.bot.message_handler(commands=COMMANDS['HELP'])
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
                pass
            elif message.text == KEYBOARD['SETTINGS']:
                self.pressed_button_settings(message)
            elif message.text == KEYBOARD['INFO']:
                self.pressed_button_info(message)
            else:
                self.check_answer(message)
