from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from typing import List, Optional


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(16), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(64))
    animals: Mapped[List["Animal"]] = relationship(
        back_populates="master",
        cascade="save-update, merge",
        passive_deletes=True,
    )

    def __init__(self, username: str):
        self.username = username


class Animal(Base):
    __tablename__ = "animal"

    id: Mapped[int] = mapped_column(primary_key=True)
    master_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    species: Mapped[str] = mapped_column(String(16))
    age: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    master: Mapped[Optional["User"]] = relationship(back_populates="animals")

    def __init__(self, species: str, age: int):
        self.species = species
        self.age = age
