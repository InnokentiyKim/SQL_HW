from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref, Mapped
from data_base.db_core import Base
from models.user import User



class Word(Base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    rus_title = Column(String, nullable=False)
    eng_title = Column(String, nullable=False)
    is_studied = Column(Integer, default=0)
    # number_of_attempts = Column(Integer, default=0)
    # successful_attempts = Column(Integer, default=0)
    # success_streak = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref('word'), cascade='delete, all')
    category = relationship("Category", secondary="category_word", back_populates="word")

    def __str__(self):
        return f"{self.rus_title} {self.eng_title} {self.is_studied}"
