from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref, Mapped
from data_base.db_core import Base
from models.bot_user import BotUser



class Word(Base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    rus_title = Column(String, index=True, nullable=False)
    eng_title = Column(String, index=True, nullable=False)
    is_studied = Column(Integer, default=0)
    number_of_attempts = Column(Integer, default=0)
    successful_attempts = Column(Integer, default=0)
    success_streak = Column(Integer, default=0)
    UniqueConstraint(rus_title, eng_title, name='rus_eng_title')
    user_id = Column(Integer, ForeignKey('bot_user.id'))
    user = relationship(BotUser, backref=backref("word"), cascade="delete, all")
    category = relationship("Category", secondary="category_word", back_populates="word")

    def __str__(self):
        return f"{self.rus_title} {self.eng_title} {self.is_studied}"
