from telebot.handler_backends import StatesGroup, State


class BotStates(StatesGroup):
    """
    Класс описывающий состояния бота.
    """
    start = State()
    play = State()
