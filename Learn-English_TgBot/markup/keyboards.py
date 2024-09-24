from telebot.types import KeyboardButton, InlineKeyboardButton


class Keyboards:
    """
    Класс для создания клавиатур.
    """

    @staticmethod
    def set_command_button(name: str):
        """
        Метод для создания кнопки с командой.
        Параметры:
            name (str): Название команды.
        Возвращает:
            KeyboardButton: Объект кнопки с командой.
        """
        return KeyboardButton(name)

    @staticmethod
    def set_word_button(name: str):
        """
        Метод для создания кнопки со словом.
        Параметры:
            name (str): Название слова.
        Возвращает:
            KeyboardButton: Объект кнопки со словом.
        """
        return KeyboardButton(name)

    @staticmethod
    def set_settings_button(name: str, data: str):
        """
        Метод для создания кнопки для настроек.
        Параметры:
            name (str): Название настройки.
            data (str): данные кнопки (полезная нагрузка)
        Возвращает:
            InlineKeyboardButton: Объект кнопки для настроек.
        """
        return InlineKeyboardButton(name, callback_data=data)
