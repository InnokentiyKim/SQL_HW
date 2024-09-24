from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from database.db_core import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional


class WordStats(Base):
    """
    Модель статистики слова.
    Атрибуты:
        id: Идентификатор статистики слова
        word_id: Идентификатор слова
        is_studied: Изучено ли слово
        number_of_attempts: Количество попыток
        successful_attempts: Количество успешных попыток
        success_streak: Успешный стрик (количество успешных попыток подряд)
        word: relationship - Слово
    """
    __tablename__ = 'word_stats'

    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(ForeignKey('word.id', ondelete='CASCADE'))
    is_studied: Mapped[int] = mapped_column(default=0)
    number_of_attempts: Mapped[int] = mapped_column(default=0)
    successful_attempts: Mapped[int] = mapped_column(default=0)
    success_streak: Mapped[int] = mapped_column(default=0)
    word: Mapped['Word'] = relationship(back_populates='word_stats')

    __tableargs__ = (
        UniqueConstraint('word_id'),
        CheckConstraint('is_studied >= 0'),
        CheckConstraint('number_of_attempts >= 0'),
        CheckConstraint('successful_attempts >= 0'),
        CheckConstraint('success_streak >= 0'),
    )
