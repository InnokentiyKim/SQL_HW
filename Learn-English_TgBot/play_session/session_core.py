from typing import Optional
from models.bot_user import BotUser
from models.word import Word
from settings.config import settings


class PlaySessionCore:
    """
    Класс сессии игры.
    Атрибуты:
        session_id: Идентификатор сессии
        user: Пользователь бота
        target_words: Список целевых слов
        target_word_index: Индекс текущего целевого слова
        current_target_word: Текущее целевое слово
        round_attempts: Количество попыток за раунд
        round_successful_attempts: Количество успешных попыток за раунд
        is_answered: Отвечен ли пользователь на текущее целевое слово
        is_target_list_ended: Кончился ли список целевых слов
        viewed_words: Список просмотренных слов
        other_words: Список "других" слов для карточек
    """
    def __init__(self):
        self.session_id: int = 0
        self.user: Optional[BotUser] = None
        self.target_words: list['Word'] = []
        self.target_word_index: int = 0
        self.current_target_word: Optional['Word'] = None
        self.round_attempts: int = 0
        self.round_successful_attempts: int = 0
        self.is_answered: bool = False
        self.is_target_list_ended: bool = True
        self.viewed_words: Optional[list[Word]] = []
        self.other_words: Optional[list[Word]] = []

    def refresh_current_word_stats(self):
        """
        Обновляет состояние текущего целевого слова.
        """
        self.is_answered = False

    def refresh_session(self):
        """
        Обновляет состояние сессии.
        """
        self.target_word_index = 0
        self.is_target_list_ended = False
        self.session_id += 1
        self.round_attempts = 0
        self.round_successful_attempts = 0

    def increase_target_words_stats(self) -> None:
        """
        Изменяет статистику и состояние целевых слов в случае успешного ответа.
        """
        self.round_attempts += 1
        self.round_successful_attempts += 1
        self.is_answered = True
        self.current_target_word.word_stats.number_of_attempts += 1
        self.current_target_word.word_stats.successful_attempts += 1
        self.current_target_word.word_stats.success_streak += 1
        if self.current_target_word.word_stats.success_streak >= settings.IS_STUDIED_COND:
            self.current_target_word.word_stats.is_studied = 1

    def decrease_target_words_stats(self) -> None:
        """
        Изменяет статистику и состояние целевых слов в случае неудачного ответа.
        """
        self.round_attempts += 1
        self.current_target_word.word_stats.number_of_attempts += 1
        self.current_target_word.word_stats.success_streak = 0

    def increase_player_stats(self) -> None:
        """
        Изменяет статистику пользователя в случае успешного ответа.
        """
        self.user.user_stats.number_of_attempts += 1
        self.user.user_stats.successful_attempts += 1
        self.user.user_stats.success_streak += 1

    def decrease_player_stats(self) -> None:
        """
        Изменяет статистику пользователя в случае неудачного ответа.
        """
        self.user.user_stats.number_of_attempts += 1
        self.user.user_stats.success_streak = 0
