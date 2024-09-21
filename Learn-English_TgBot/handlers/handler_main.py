from telebot.types import Message, CallbackQuery
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

    def pressed_button_settings(self, message: Message):
        self.get_user_settings(message)

    def pressed_button_get_hint(self, message: Message):
        self.get_hint(message)

    def pressed_button_info(self, message: Message):
        self.get_info(message)

    def pressed_button_back(self, message: Message):
        self.get_step_back(message)

    def pressed_button_next(self, message: Message):
        self.get_next_card(message, play_mode=self.play_session.user.user_settings.translation_mode)

    def pressed_button_notification(self, call: CallbackQuery):
        self.change_notification_state(call)


    def handle(self):
        @self.bot.message_handler(commands=COMMANDS['HELP'])
        def handle(message):
            self.pressed_button_help(message)

        @self.bot.message_handler(commands=[COMMANDS['START']])
        def handle(message):
            self.pressed_button_start(message)

        @self.bot.message_handler(commands=[COMMANDS['CARDS']])
        def handle(message):
            self.pressed_button_cards(message)

        @self.bot.message_handler(commands=[COMMANDS['INFO']])
        def handle(message):
            self.pressed_button_info(message)

        @self.bot.message_handler(commands=COMMANDS['ADD_WORD'])
        def handle_add_new_word(message):
            self.bot.send_message(message.chat.id, "Введите слово на русском: ")
            self.bot.register_next_step_handler(message, get_rus_word)

        def get_rus_word(message):
            rus_word = message.text
            is_valid_word = self.validate_input_word(rus_word)
            if is_valid_word:
                self.new_users_word['rus_title'] = rus_word
                self.bot.register_next_step_handler(message, get_eng_word)
                self.bot.send_message(message.chat.id, "Введите слово на английском: ")
            else:
                self.bot.send_message(message.chat.id, "Неверный формат слова. Введите слово на русском: ")

        def get_eng_word(message):
            eng_word = message.text
            is_valid_word = self.validate_input_word(eng_word)
            if is_valid_word:
                self.new_users_word['eng_title'] = eng_word
                self.bot.register_next_step_handler(message, get_category)
                self.bot.send_message(message.chat.id, "Введите категорию (<i>all</i> или <i>все</i> - <i>Общая</i> категория): ",
                                      parse_mode='html')
            else:
                self.bot.send_message(message.chat.id, "Неверный формат слова. Введите слово на английском: ")

        def get_category(message):
            category_name = message.text
            is_valid_category = self.validate_input_word(category_name)
            if is_valid_category:
                self.new_users_word['category_name'] = category_name
                self.add_new_word(
                    message=message, rus_title=self.new_users_word['rus_title'],
                    eng_title=self.new_users_word['eng_title'], category_name=self.new_users_word['category_name']
                )
            else:
                self.bot.send_message(message.chat.id, "Неверный формат категории. Введите категорию "
                                                       "(<i>all</i> или <i>все</i> - <i>Общая</i> категория): ", parse_mode='html')

        @self.bot.message_handler(commands=COMMANDS['DELETE_WORD'])
        def handle_delete_word(message):
            self.bot.send_message(message.chat.id, "Введите слово на русском или на английском: ")
            self.bot.register_next_step_handler(message, get_deleting_word)

        def get_deleting_word(message):
            deleting_word = message.text
            is_valid_word = self.validate_input_word(deleting_word)
            if is_valid_word:
                self.delete_word(message, deleting_word)
            else:
                self.bot.send_message(message.chat.id, "Неверный формат слова. "
                                                       "Введите слово на русском или на английском: ")

        @self.bot.callback_query_handler(func=lambda call: call.data == KEYBOARD['NOTIFICATION'])
        def handle_notification_pressed(call: CallbackQuery):
            self.pressed_button_notification(call)


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
            else:
                self.check_answer(message, self.play_session.user.user_settings.translation_mode)
