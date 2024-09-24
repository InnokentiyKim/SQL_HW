from telebot.types import Message, CallbackQuery
from handlers.handler_functions import HandlerFunctions
from settings.config import COMMANDS, KEYBOARD, settings
from handlers.bot_states import BotStates


class HandlerMain(HandlerFunctions):
    def __init__(self, bot):
        super().__init__(bot)
        self.user_states = {}

    def pressed_button_help(self, message: Message):
        self.get_help(message)

    def pressed_button_start(self, message: Message):
        self.start_actions(message)
        self.user_states[message.chat.id] = BotStates.start

    def pressed_button_cards(self, message: Message):
        if message.chat.id not in self.user_states:
            self.pressed_button_start(message)
        self.user_states[message.chat.id] = BotStates.play
        self.get_next_card(message, play_mode=self.play_session.user.user_settings.translation_mode)

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

    def pressed_button_show_user_statistics(self, message: Message):
        self.show_user_statistics(message)

    def pressed_button_notification(self, call: CallbackQuery):
        self.change_notification_state(call)

    def pressed_button_change_translation_mode(self, call: CallbackQuery):
        self.change_translation_mode(call)

    def pressed_button_change_words_chunk_size(self, message: Message):
        self.change_words_chunk_size(message)

    def pressed_button_reset_settings(self, call: CallbackQuery):
        self.reset_all_settings(call)


    def handle(self):
        @self.bot.message_handler(commands=[COMMANDS['HELP']])
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

        @self.bot.message_handler(commands=[COMMANDS['ADD_WORD']])
        def handle_add_new_word(message):
            if message.chat.id not in self.user_states:
                self.pressed_button_start(message)
            if self.user_states[message.chat.id] == BotStates.play:
                self.bot.send_message(message.chat.id, "Введите слово на русском: ")
                self.bot.register_next_step_handler(message, get_rus_word)

        def get_rus_word(message):
            rus_word = message.text
            is_valid_word = self.validate_input_word(rus_word, language='rus')
            if is_valid_word:
                self.new_users_word['rus_title'] = rus_word
                self.bot.register_next_step_handler(message, get_eng_word)
                self.bot.send_message(message.chat.id, "Введите слово на английском: ")
            else:
                self.bot.send_message(message.chat.id, "Неверный формат слова. Попробуйте снова")
                self.bot.register_next_step_handler(message, get_rus_word)

        def get_eng_word(message):
            eng_word = message.text
            is_valid_word = self.validate_input_word(eng_word, language='eng')
            if is_valid_word:
                self.new_users_word['eng_title'] = eng_word
                self.bot.register_next_step_handler(message, get_category)
                self.bot.send_message(message.chat.id, "Введите категорию (<i>all</i> или <i>все</i> - <i>Общая</i> категория): ",
                                      parse_mode='html')
            else:
                self.bot.send_message(message.chat.id, "Неверный формат слова. Попробуйте снова")
                self.bot.register_next_step_handler(message, get_eng_word)

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
                self.bot.send_message(message.chat.id, "Неверный формат категории. Попробуйте снова")
                self.bot.register_next_step_handler(message, get_category)

        @self.bot.message_handler(commands=[COMMANDS['DELETE_WORD']])
        def handle_delete_word(message):
            if message.chat.id not in self.user_states:
                self.pressed_button_start(message)
            if self.user_states[message.chat.id] == BotStates.play:
                self.bot.send_message(message.chat.id, "Введите слово на русском или на английском: ")
                self.bot.register_next_step_handler(message, get_deleting_word)

        def get_deleting_word(message):
            deleting_word = message.text
            is_valid_word = self.validate_input_word(deleting_word)
            if is_valid_word:
                self.delete_word(message, deleting_word)
            else:
                self.bot.send_message(message.chat.id, "Неверный формат слова. Попробуйте снова")
                self.bot.register_next_step_handler(message, get_deleting_word)


        @self.bot.callback_query_handler(func=lambda call: call.data == KEYBOARD['NOTIFICATION'])
        def handle_notification_pressed(call: CallbackQuery):
            self.pressed_button_notification(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == KEYBOARD['TRANSLATION_MODE'])
        def handle_change_translation_mode(call: CallbackQuery):
            self.pressed_button_change_translation_mode(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == KEYBOARD['WORDS_CHUNK_SIZE'])
        def handle_change_words_chunk_size(call: CallbackQuery):
            self.bot.send_message(
                chat_id=call.message.chat.id, text=f"Введите количество слов раунда "
                                                   f"(число от {settings.MIN_WORDS_CHUNK_SIZE} "
                                                   f"до {settings.OTHER_WORDS_CHUNK_SIZE}): "
            )
            self.bot.register_next_step_handler(call.message, get_words_chunk_size)

        @self.bot.callback_query_handler(func=lambda call: call.data == KEYBOARD['RESET_SETTINGS'])
        def handle_reset_settings(call: CallbackQuery):
            self.pressed_button_reset_settings(call)

        def get_words_chunk_size(message):
            self.pressed_button_change_words_chunk_size(message)


        @self.bot.message_handler(func=lambda message: True)
        def handle_text(message):
            if message.chat.id not in self.user_states:
                self.user_states[message.chat.id] = BotStates.start
                self.pressed_button_start(message)
            if self.user_states[message.chat.id] == BotStates.play:
                if message.text == KEYBOARD['NEXT_STEP']:
                    self.pressed_button_next(message)
                elif message.text == KEYBOARD['SETTINGS']:
                    self.pressed_button_settings(message)
                elif message.text == KEYBOARD['HINT']:
                    self.pressed_button_get_hint(message)
                elif message.text == KEYBOARD['BACK']:
                    self.pressed_button_back(message)
                elif message.text == KEYBOARD['USER_STATISTICS']:
                    self.pressed_button_show_user_statistics(message)
                else:
                    self.check_answer(message, self.play_session.user.user_settings.translation_mode)
