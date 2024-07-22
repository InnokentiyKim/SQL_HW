from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from data_base.db_core import Base
from models.user import User


class Word(Base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    rus_title = Column(String, nullable=False)
    eng_title = Column(String, nullable=False)
    is_studied = Column(Boolean, default=False)
    number_of_attempts = Column(Integer)
    successful_attempts = Column(Integer)
    success_streak = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref('word'), uselist=True, cascade='delete, all')

    def __str__(self):
        return f"{self.rus_title} {self.eng_title} {self.is_studied}"
