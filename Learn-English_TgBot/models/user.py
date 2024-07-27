from sqlalchemy import Column, String, Integer, BigInteger
from data_base.db_core import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, index=True, nullable=False)
    # number_of_attempts = Column(Integer, default=0)
    # successful_attempts = Column(Integer, default=0)
    # success_streak = Column(Integer, default=0)

    def __str__(self):
        return f"{self.id} {self.name}"