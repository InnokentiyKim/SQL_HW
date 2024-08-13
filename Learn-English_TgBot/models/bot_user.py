from sqlalchemy.orm import Mapped, mapped_column, relationship
from data_base.db_core import Base
from typing import Optional


class BotUser(Base):
    __tablename__ = 'bot_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(default=f'User {id}')
    number_of_attempts: Mapped[Optional[int]] = mapped_column(default=0)
    successful_attempts: Mapped[Optional[int]] = mapped_column(default=0)
    success_streak: Mapped[Optional[int]] = mapped_column(default=0)
    word: Mapped[list['Word']] = relationship(back_populates='bot_user')

    def __str__(self):
        return f"{self.id} {self.name}"
