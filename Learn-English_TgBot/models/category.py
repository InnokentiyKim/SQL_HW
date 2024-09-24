from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db_core import Base
from models.category_word import CategoryWord
from settings.config import CATEGORIES


class Category(Base):
    """
    Модель категории.
    Атрибуты:
        id: Идентификатор категории
        name: Название категории
        word: relationship - Слова категории
    """
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default=CATEGORIES['COMMON']['name'])

    word: Mapped[list['Word']] = relationship(secondary='category_word', back_populates='category')

    __table_args__ = (
        UniqueConstraint('name'),
        Index('category_name_idx', 'name'),
    )

    def __str__(self):
        return f"{self.id} {self.name}"
