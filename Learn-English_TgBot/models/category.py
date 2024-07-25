from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship, backref, Mapped
from data_base.db_core import Base
from models.category_word import CategoryWord
from models.word import Word


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, default=1)
    eng_name = Column(String, unique=True, index=True, default='common')
    rus_name = Column(String, unique=True, index=True, default='общие')
    word = relationship("Word", secondary="category_word", back_populates="category")
    # word_rel: Mapped[list["Word"]] = relationship(Word, back_populates="word", secondary="category_word")

    def __str__(self):
        return f"{self.eng_name} {self.rus_name}"
