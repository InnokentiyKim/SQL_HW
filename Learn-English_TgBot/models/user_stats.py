from sqlalchemy import ForeignKey, CheckConstraint
from database.db_core import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserStats(Base):
    """
    Модель статистики пользователя.
    Атрибуты:
        id: Идентификатор статистики пользователя
        number_of_attempts: Количество попыток
        successful_attempts: Количество успешных попыток
        success_streak: Успешный стрик (количество успешных попыток подряд)
        bot_user: relationship - Пользователь бота
    """
    __tablename__ = 'user_stats'

    id: Mapped[int] = mapped_column(ForeignKey('bot_user.id', ondelete='CASCADE'), primary_key=True)
    number_of_attempts: Mapped[int] = mapped_column(default=0)
    successful_attempts: Mapped[int] = mapped_column(default=0)
    success_streak: Mapped[int] = mapped_column(default=0)
    bot_user: Mapped['BotUser'] = relationship(back_populates='user_stats')

    __tableargs__ = (
        CheckConstraint('number_of_attempts >= 0'),
        CheckConstraint('successful_attempts >= 0'),
        CheckConstraint('success_streak >= 0'),
    )
