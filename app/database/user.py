from datetime import datetime
from typing import Optional

from sqlalchemy import String, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    fullname: Mapped[Optional[str]]

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
