from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db_core import Base
from typing import Optional

from settings.config import CATEGORIES


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default=CATEGORIES['COMMON']['name'])
    word: Mapped[list['Word']] = relationship(secondary='category_word', back_populates='category')

    __table_args__ = (
        UniqueConstraint('name'),
    )

    def __str__(self):
        return f"{self.id} {self.name}"
