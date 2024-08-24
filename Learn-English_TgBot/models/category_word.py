from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from data_base.db_core import Base


class CategoryWord(Base):
    __tablename__ = 'category_word'

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'))
    word_id: Mapped[int] = mapped_column(ForeignKey('word.id', ondelete='CASCADE'))

    __table_args__ = (
        PrimaryKeyConstraint(category_id, word_id),
    )
