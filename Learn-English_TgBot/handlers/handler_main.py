from telebot.types import Message
from handlers.handler_functions import HandlerFunctions
from models.bot_user import BotUser
from settings.config import COMMANDS, KEYBOARD
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


class HandlerMain(HandlerFunctions):
    def __init__(self, bot):
        super().__init__(bot)
        self.users = {}

    def pressed_button_help(self, message: Message):
        self.get_help(message)

    def pressed_button_start(self, message: Message):
        self.start_actions(message)

    def pressed_button_cards(self, message: Message):
        self.get_next_card(message, play_mode=self.play_session.user.user_settings.translation_mode)

    # def pressed_button_menu(self, message: Message):
    #     self.get_bots_menu(message)

    def pressed_button_add_word(self, message: Message, user: BotUser, rus_word: str, eng_word: str, category: str):
        self.add_new_word(message, user=user, rus_title=rus_word, eng_title=eng_word, category_name=category)

    def pressed_button_delete_word(self, message: Message, word):
        self.delete_word(message, word)

    def pressed_button_settings(self, message: Message):
        pass

    def pressed_button_get_hint(self, message: Message):
        self.get_hint(message)

    def pressed_button_info(self, message: Message):
        self.get_info(message)

    def pressed_button_back(self, message: Message):
        self.get_step_back(message)

    def pressed_button_next(self, message: Message):
        self.get_next_card(message, play_mode=self.play_session.user.user_settings.translation_mode)


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

        @self.bot.message_handler(commands=[COMMANDS['INFO']])
        def handle(message):
            if message.text == '/info':
                self.pressed_button_info(message)

        @self.bot.message_handler(func=lambda message: message.text == COMMANDS['ADD_WORD'])
        def handle_add_new_word(message):
            if message.text == '/add_word':
                chat_id = message.chat.id
                self.bot.send_message(chat_id, "Введите слово на русском: ")
                self.users[chat_id] = {}
                # self.bot.register_next_step_handler(message, get_rus_word)

        # def get_rus_word(message):
        #     chat_id = message.chat.id
        #     self.users[chat_id]['rus'] = message.text
        #     self.bot.send_message(chat_id, "Введите слово на английском: ")
        #     self.bot.register_next_step_handler(message, get_eng_word)
        #
        # def get_eng_word(message):
        #     chat_id = message.chat.id
        #     self.users[chat_id]['eng'] = message.text
        #     self.bot.send_message(chat_id, "Введите категорию: ")
        #     self.bot.register_next_step_handler(message, get_category)
        #
        # def get_category(message):
        #     chat_id = message.chat.id
        #     self.users[chat_id]['category'] = message.text
        #     self.pressed_button_add_word(message, self.users[chat_id]['rus'], self.users[chat_id]['eng'],
        #                                  self.users[chat_id]['category'])

        @self.bot.message_handler(func=lambda message: message.text == COMMANDS['DELETE_WORD'])
        def handle_delete_word(message):
            if message.text == '/delete_word':
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
            elif message.text == KEYBOARD['SETTINGS']:
                self.pressed_button_settings(message)
            elif message.text == KEYBOARD['HINT']:
                self.pressed_button_get_hint(message)
            elif message.text == KEYBOARD['BACK']:
                self.pressed_button_back(message)
            elif message.text == KEYBOARD['ADD_WORD']:
                pass
            elif message.text == KEYBOARD['DELETE_WORD']:
                pass
            else:
                self.check_answer(message, self.play_session.user.user_settings.translation_mode)
