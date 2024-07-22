from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship, backref
from data_base.db_core import Base
from models.word import Word
from category_word import category_word


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    rus_name = Column(String, unique=True, nullable=False)
    eng_name = Column(String, unique=True, nullable=False)
    word = relationship(Word, secondary=category_word, backref=backref('word'), cascade='delete, all')

    def __str__(self):
        return f"{self.name} {self.title} {self.price}"