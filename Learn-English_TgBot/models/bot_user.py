from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db_core import Base
from typing import Optional
from models.user_settings import UserSettings
from models.user_stats import UserStats


class BotUser(Base):
    __tablename__ = 'bot_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(default=f'User {id}')
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    last_seen_at: Mapped[datetime] = mapped_column(default=datetime.now())
    user_stats: Mapped['UserStats'] = relationship(back_populates='bot_user', uselist=False)
    user_settings: Mapped['UserSettings'] = relationship(back_populates='bot_user', uselist=False)
    word: Mapped[list['Word']] = relationship(back_populates='bot_user')

    def __str__(self):
        return f"{self.id} {self.name}"
