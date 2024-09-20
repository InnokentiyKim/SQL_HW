from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db_core import Base


class CategoryWord(Base):
    __tablename__ = 'category_word'
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'))
    word_id: Mapped[int] = mapped_column(ForeignKey('word.id', ondelete='CASCADE'))
    word_details: Mapped['Word'] = relationship(back_populates='words_category')
    category_details: Mapped['Category'] = relationship(back_populates='categories_word')

    __table_args__ = (
        UniqueConstraint('category_id', 'word_id'),
    )
