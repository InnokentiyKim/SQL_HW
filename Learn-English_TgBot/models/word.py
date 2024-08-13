from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from data_base.db_core import Base
from models.bot_user import BotUser
from models.category import Category
from typing import Optional


class Word(Base):
    __tablename__ = 'word'

    id: Mapped[int] = mapped_column(primary_key=True)
    rus_title: Mapped[str] = mapped_column(index=True, nullable=False)
    eng_title: Mapped[str] = mapped_column(index=True, nullable=False)
    is_studied: Mapped[Optional[int]] = mapped_column(default=0)
    number_of_attempts: Mapped[Optional[int]] = mapped_column(default=0)
    successful_attempts: Mapped[Optional[int]] = mapped_column(default=0)
    success_streak: Mapped[Optional[int]] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey('bot_user.id', ondelete='CASCADE'))
    user: Mapped['BotUser'] = relationship(back_populates='word')
    category: Mapped[list['Category']] = relationship(secondary='category_word', back_populates='word')

    __tableargs__ = (
        UniqueConstraint('rus_title', 'eng_title'),
    )

    def __str__(self):
        return f"{self.rus_title} {self.eng_title} {self.is_studied}"
