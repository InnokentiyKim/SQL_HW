from handlers.handler import Handler
from settings.message import MESSAGES
from settings.config import COMMANDS


class HandlerCommands(Handler):

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        self.bot.send_message(message.chat.id, f"{message.from_user.first_name}, {MESSAGES['START']}", reply_markup=self.keyboards.cards_desk())

    def handle(self):
        @self.bot.message_handler(commands=[COMMANDS['START']])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)