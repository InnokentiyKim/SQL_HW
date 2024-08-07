from sqlalchemy import Column, String, Integer
from data_base.db_core import Base


class BotUser(Base):
    __tablename__ = 'bot_user'

    id = Column(Integer, primary_key=True)
    name = Column(String, default=f"User")
    number_of_attempts = Column(Integer, default=0)
    successful_attempts = Column(Integer, default=0)
    success_streak = Column(Integer, default=0)

    def __str__(self):
        return f"{self.id} {self.name}"
