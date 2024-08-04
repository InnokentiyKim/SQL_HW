from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from data_base.db_core import Base


class CategoryWord(Base):
    __tablename__ = 'category_word'

    category_id = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'))
    word_id = Column(Integer, ForeignKey('word.id', ondelete='CASCADE'))
    PrimaryKeyConstraint(category_id, word_id)
