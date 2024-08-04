from handlers.handler import Handler
from settings.config import COMMANDS, KEYBOARD
from settings.message import MESSAGES


class HandlerMain(Handler):
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_button_help(self, message):
        self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['HELP']}", parse_mode='html')

    def pressed_button_start(self, message):
        self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['START']}")

    def pressed_button_cards(self, message):
        user_id = int(message.from_user.id)
        if not self.DB.identified_user(user_id):
            self.DB.init_default_cards(user_id)
        main_keyboard = self.keyboards.get_next_word_keyboard(user_id)
        self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']} "
                                               f"{self.DB.target_word.rus_title}", reply_markup=main_keyboard)

    def pressed_button_menu(self, message):
        user_id = int(message.from_user.id)
        menu_keyboard = self.keyboards.get_menu_keyboard()
        self.bot.send_message(message.chat.id, f"{KEYBOARD['MENU']}", reply_markup=menu_keyboard)
        return menu_keyboard

    def pressed_button_add_word(self, message):
        user_id = int(message.from_user.id)
        self.DB.add_word(user_id)

    def pressed_button_delete_word(self, message):
        user_id = int(message.from_user.id)
        self.DB.delete_word(user_id)

    def pressed_button_settings(self, message):
        pass

    def pressed_button_info(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['INFO'], parse_mode='html')

    def pressed_button_back(self, message):
        main_keyboard = self.keyboards.active_keyboard
        self.bot.send_message(message.chat.id, f"{KEYBOARD['MENU']}", reply_markup=main_keyboard)

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
            if message.text == KEYBOARD['NEXT_STEP']:
                self.pressed_button_next(message)
            elif message.text == KEYBOARD['MENU']:
                self.pressed_button_menu(message)
            elif message.text == KEYBOARD['BACK']:
                self.pressed_button_back(message)
            elif message.text == KEYBOARD['ADD_WORD']:
                self.pressed_button_add_word(message)
            elif message.text == KEYBOARD['DELETE_WORD']:
                self.pressed_button_delete_word(message)
            elif message.text == KEYBOARD['SETTINGS']:
                self.pressed_button_settings(message)
            elif message.text == KEYBOARD['INFO']:
                self.pressed_button_info(message)
            else:
                self.check_answer(message)
