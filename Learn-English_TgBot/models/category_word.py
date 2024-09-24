from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db_core import Base


class CategoryWord(Base):
    """
    Модель связи категории и слова.
    Атрибуты:
        id: Идентификатор связи
        category_id: Идентификатор категории
        word_id: Идентификатор слова
    """
    __tablename__ = 'category_word'
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'))
    word_id: Mapped[int] = mapped_column(ForeignKey('word.id', ondelete='CASCADE'))

    __table_args__ = (
        UniqueConstraint('category_id', 'word_id'),
    )
