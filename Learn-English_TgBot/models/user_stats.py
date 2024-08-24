from sqlalchemy import ForeignKey, CheckConstraint
from data_base.db_core import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


class UserStats(Base):
    __tablename__ = 'user_stats'

    id: Mapped[int] = mapped_column(ForeignKey('bot_user.id', ondelete='CASCADE'), primary_key=True)
    number_of_attempts: Mapped[Optional[int]] = mapped_column(default=0)
    successful_attempts: Mapped[Optional[int]] = mapped_column(default=0)
    success_streak: Mapped[Optional[int]] = mapped_column(default=0)

    __tableargs__ = (
        CheckConstraint()
    )
