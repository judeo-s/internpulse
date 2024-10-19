from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
"""
This module is dedicated to defining the database metadata in sqlalchemy.
"""


class Base(DeclarativeBase):
    """
    This class acts as the decarative base.
    """
    pass


class Products(Base):
    """
    A class to represent the Products table in the database
    """
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
