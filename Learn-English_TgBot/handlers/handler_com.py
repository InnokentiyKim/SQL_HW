from handlers.handler import Handler
from settings.message import MESSAGES
from settings.config import COMMANDS, KEYBOARD


class HandlerCommands(Handler):

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['START']}")

    def pressed_btn_cards(self, message):
        main_keyboard = self.keyboards.get_next_word_keyboard(1)
        self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']} "
                                               f"{self.DB.target_word.rus_title}",
                              reply_markup=main_keyboard)


    def handle(self):
        @self.bot.message_handler(commands=[COMMANDS['START']])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)

        @self.bot.message_handler(commands=[COMMANDS['CARDS']])
        def handle(message):
            if message.text == '/cards':
                self.pressed_btn_cards(message)


