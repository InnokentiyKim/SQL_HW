from settings.message import MESSAGES
from settings import config
from handlers.handler import Handler


class HandlerAllText(Handler):

    def __init__(self, bot):
        super().__init__(bot)

    # def pressed_button_info(self, message):
    #     self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
    #                           parse_mode="HTML", reply_markup=self.keyboards.info_menu())
    #
    # def pressed_button_settings(self, message):
    #     self.bot.send_message(message.chat.id, MESSAGES['settings'],
    #                           parse_mode="HTML", reply_markup=self.keyboards.settings_menu())
    #
    def pressed_button_back(self, message):
        self.bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=self.keyboards.start_menu())

    def handle(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            pass
            # if message.text == config.KEYBOARD['INFO']:
            #     self.pressed_button_info(message)
            # if message.text == config.KEYBOARD['SETTINGS']:
            #     self.pressed_button_settings(message)
            # if message.text == config.KEYBOARD['<<']:
            #     self.pressed_button_back(message)