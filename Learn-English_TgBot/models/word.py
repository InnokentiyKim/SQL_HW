from sqlalchemy import ForeignKey, UniqueConstraint, Index, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.db_core import Base
from models.bot_user import BotUser
from models.category import Category
from models.category_word import CategoryWord
from models.word_stats import WordStats


class Word(Base):
    """
    Модель слова.
    Атрибуты:
        id: Идентификатор слова
        rus_title: Русское название слова
        eng_title: Английское название слова
        user_id: Идентификатор пользователя
        bot_user: relationship - Пользователь бота
        word_stats: relationship - Статистика слова
        category: relationship - Категории слова
    """
    __tablename__ = 'word'

    id: Mapped[int] = mapped_column(primary_key=True)
    rus_title: Mapped[str] = mapped_column(index=True, nullable=False)
    eng_title: Mapped[str] = mapped_column(index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('bot_user.id', ondelete='CASCADE'))

    bot_user: Mapped['BotUser'] = relationship(back_populates='word')
    word_stats: Mapped['WordStats'] = relationship(back_populates='word', uselist=False, cascade='all, delete-orphan')
    category: Mapped[list['Category']] = relationship(secondary='category_word', back_populates='word')

    __tableargs__ = (
        UniqueConstraint(rus_title, eng_title),
    )

    def __str__(self):
        return f"{self.rus_title} {self.eng_title}"
