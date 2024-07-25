from sqlalchemy import Table, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint
from data_base.db_core import Base


class CategoryWord(Base):
    __tablename__ = 'category_word'

    # id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'), primary_key=True)
    word_id = Column(Integer, ForeignKey('word.id', ondelete='CASCADE'), primary_key=True)
    # __table_args__ = (PrimaryKeyConstraint(category_id, word_id), {})


# CategoryWord = Table(
#     'category_word', Base.metadata,
#     Column('category_id', Integer(), ForeignKey('category.id', ondelete='CASCADE'), primary_key=True),
#     Column('word_id', Integer(), ForeignKey('word.id', ondelete='CASCADE'), primary_key=True)
# )
