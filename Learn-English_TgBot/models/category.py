from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from data_base.db_core import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, default="общие")
    word = relationship("Word", secondary="category_word", back_populates="category")

    def __str__(self):
        return f"{self.eng_name} {self.rus_name}"
