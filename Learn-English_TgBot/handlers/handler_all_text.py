from settings.message import MESSAGES, KEYBOARD
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
        self.bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=self.keyboards.active_keyboard)

    def pressed_button_next(self, message):
        main_keyboard = self.keyboards.get_next_word_keyboard(1)
        self.bot.send_message(message.chat.id, f"{MESSAGES['NEXT_WORD']} {KEYBOARD['RUS']} "
                                               f"{self.DB.target_word.rus_title}",
                              reply_markup=main_keyboard)

    def check_answer(self, message):
        answer = str(message.text).lower()
        if self.DB.target_word.eng_title == answer:
            self.bot.send_message(message.chat.id, "Правильно", reply_markup=self.keyboards.active_keyboard)
        else:
            self.bot.send_message(message.chat.id, "К сожалению, вы ошиблись. Попробуйте снова", reply_markup=self.keyboards.active_keyboard)

    def handle(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_button_next(message)
            else:
                self.check_answer(message)
            # if message.text == config.KEYBOARD['INFO']:
            #     self.pressed_button_info(message)
            # if message.text == config.KEYBOARD['SETTINGS']:
            #     self.pressed_button_settings(message)
