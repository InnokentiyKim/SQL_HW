from sqlalchemy.orm import Mapped, mapped_column, relationship
from data_base.db_core import Base
from typing import Optional


class BotUser(Base):
    __tablename__ = 'bot_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(default=f'User {id}')
    user_stats: Mapped['UserStats'] = relationship(back_populates='bot_user')
    word: Mapped[list['Word']] = relationship(back_populates='bot_user')

    def __str__(self):
        return f"{self.id} {self.name}"
