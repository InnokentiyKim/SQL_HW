from sqlalchemy import ForeignKey, CheckConstraint
from database.db_core import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.config import TranslationMode, settings


class UserSettings(Base):
    """
    Модель настроек пользователя.
    Атрибуты:
        id: Идентификатор настроек пользователя
        notification: Уведомления
        translation_mode: Режим перевода
        words_chunk_size: Размер блока слов
        bot_user: relationship - Пользователь бота
    """
    __tablename__ = 'user_settings'

    id: Mapped[int] = mapped_column(ForeignKey('bot_user.id', ondelete='CASCADE'), primary_key=True)
    notification: Mapped[int] = mapped_column(default=0)
    translation_mode: Mapped[TranslationMode] = mapped_column(default=TranslationMode.RUS_TO_ENG)
    words_chunk_size: Mapped[int] = mapped_column(default=settings.TARGET_WORDS_CHUNK_SIZE)
    bot_user: Mapped['BotUser'] = relationship(back_populates='user_settings')

    __tableargs__ = (
        CheckConstraint('notification >= 0'),
        CheckConstraint('words_chuck_size > 0'),
        CheckConstraint('words_chuck_size < 50'),
    )
