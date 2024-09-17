from sqlalchemy import ForeignKey, CheckConstraint
from database.db_core import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.config import TranslationMode


class UserSettings(Base):
    __tablename__ = 'user_settings'

    id: Mapped[int] = mapped_column(ForeignKey('bot_user.id', ondelete='CASCADE'), primary_key=True)
    notification: Mapped[int] = mapped_column(default=0)
    translation_mode: Mapped[TranslationMode] = mapped_column(default=TranslationMode.RUS_TO_ENG)
    bot_user: Mapped['BotUser'] = relationship(back_populates='user_settings')
