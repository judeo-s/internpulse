from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

"""
This module defines the database metadata using SQLAlchemy.
The Base class serves as the declarative base for metadata classes.
"""

class Base(DeclarativeBase):
    """
    This class acts as the declarative base for SQLAlchemy metadata classes.
    """
    pass

class Products(Base):
    """
    A class representing the Products table in the database.
    """
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    def __repr__(self) -> str:
        """
        Return a string representation of the Products instance.
        """
        return f"Products(id={self.id!r}, name={self.name!r})"

