from datetime import datetime, UTC
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db_core import Base
from typing import Optional
from models.user_settings import UserSettings
from models.user_stats import UserStats


class BotUser(Base):
    """
    Модель пользователя бота.
    Атрибуты:
        id: Идентификатор пользователя
        name: Имя пользователя
        created_at: Дата создания пользователя
        last_seen_at: Дата последнего посещения пользователя
        user_stats: relationship - Статистика пользователя
        user_settings: relationship - Настройки пользователя
        word: relationship - Слова пользователя
    """
    __tablename__ = 'bot_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(default=f'User {id}')
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC), nullable=False)

    user_stats: Mapped['UserStats'] = relationship(back_populates='bot_user', uselist=False, cascade='all, delete-orphan')
    user_settings: Mapped['UserSettings'] = relationship(back_populates='bot_user', uselist=False, cascade='all, delete-orphan')
    word: Mapped[list['Word']] = relationship(back_populates='bot_user')

    def __str__(self):
        return f"{self.id} {self.name}"
