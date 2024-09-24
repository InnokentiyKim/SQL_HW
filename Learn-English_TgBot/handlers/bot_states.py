from telebot.handler_backends import StatesGroup, State


class BotStates(StatesGroup):
    start = State()
    play = State()
