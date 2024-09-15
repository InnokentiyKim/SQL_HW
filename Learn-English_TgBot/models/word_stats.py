from sqlalchemy import ForeignKey, CheckConstraint
from database.db_core import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional


class WordStats(Base):
    __tablename__ = 'word_stats'

    id: Mapped[int] = mapped_column(ForeignKey('bot_user.id', ondelete='CASCADE'), primary_key=True)
    is_studied: Mapped[int] = mapped_column(default=0)
    number_of_attempts: Mapped[int] = mapped_column(default=0)
    successful_attempts: Mapped[int] = mapped_column(default=0)
    success_streak: Mapped[int] = mapped_column(default=0)
    word: Mapped['Word'] = relationship(back_populates='word_stats')

    __tableargs__ = (
        CheckConstraint('is_studied >= 0'),
        CheckConstraint('number_of_attempts >= 0'),
        CheckConstraint('successful_attempts >= 0'),
        CheckConstraint('success_streak >= 0'),
    )
