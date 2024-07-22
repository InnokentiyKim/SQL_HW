from sqlalchemy import Table, Column, String, Integer, Boolean, ForeignKey
from data_base.db_core import Base


category_word = Table(
    'category_word', Base.metadata,
    Column('category_id_word_id', primary_key=True),
    Column('category_id', Integer(), ForeignKey('category.id')),
    Column('word_id', Integer(), ForeignKey('word.id'))
)
