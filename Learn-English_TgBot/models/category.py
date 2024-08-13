from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data_base.db_core import Base
from typing import Optional


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(default='общие')
    word: Mapped[list['Word']] = relationship(secondary='category_word', back_populates='category')

    __table_args__ = (
        UniqueConstraint('name'),
        Index('name'),
    )

    def __str__(self):
        return f"{self.id} {self.name}"
