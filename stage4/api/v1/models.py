from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer
from datetime import datetime
"""
This module defines the database metadata using SQLAlchemy.
The Base class serves as the declarative base for metadata classes.
"""


class Library(DeclarativeBase):
    """
    This class acts as the declarative base for SQLAlchemy metadata classes.
    """
    pass


class Books(Library):
    """
    A class representing the Books table in the database.
    """
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    genre: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    publication_date: Mapped[str] = mapped_column(String, nullable=False)
    availability_status: Mapped[str] = mapped_column(String(15), nullable=False)
    edition: Mapped[str] = mapped_column(String(30), nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(String(30), nullable=False, default=lambda: datetime.utcnow().isoformat() + 'Z')
    updated_at: Mapped[str] = mapped_column(String(30), nullable=False, default=lambda: datetime.utcnow().isoformat() + 'Z', onupdate=lambda: datetime.utcnow().isoformat() + 'Z')

    def __repr__(self) -> str:
        """
        Return a string representation of the Books instance.
        """
        return (f"Books(id={self.id!r}, title={self.title!r}, author={self.author!r}, "
                f"description={self.description!r}, genre={self.genre!r}, "
                f"publication_date={self.publication_date!r}, availability_status={self.availability_status!r}, "
                f"edition={self.edition!r}, summary={self.summary!r}, "
                f"created_at={self.created_at!r}, updated_at={self.updated_at!r})")
