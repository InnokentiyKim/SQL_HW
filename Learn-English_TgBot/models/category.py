from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from data_base.db_core import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    eng_name = Column(String, default="common")
    rus_name = Column(String, default="общие")
    UniqueConstraint(eng_name, rus_name, name='eng_rus_name')
    word = relationship("Word", secondary="category_word", back_populates="category")

    def __str__(self):
        return f"{self.eng_name} {self.rus_name}"
