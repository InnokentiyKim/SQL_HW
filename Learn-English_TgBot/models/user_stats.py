from sqlalchemy import ForeignKey, CheckConstraint
from database.db_core import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserStats(Base):
    __tablename__ = 'user_stats'

    id: Mapped[int] = mapped_column(ForeignKey('bot_user.id', ondelete='CASCADE'), primary_key=True)
    number_of_attempts: Mapped[int] = mapped_column(default=0)
    successful_attempts: Mapped[int] = mapped_column(default=0)
    success_streak: Mapped[int] = mapped_column(default=0)
    bot_user: Mapped['BotUser'] = relationship(back_populates='user_stats')

    # __tableargs__ = (
    #     CheckConstraint('number_of_attempts >= 0'),
    #     CheckConstraint('successful_attempts >= 0'),
    #     CheckConstraint('success_streak >= 0'),
    # )
