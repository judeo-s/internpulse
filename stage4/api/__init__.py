from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from api.models import Library
"""
Module that acts as base for other modules.
"""


engine = create_engine("sqlite:///library.db")
Library.metadata.create_all(engine)
session = Session(engine)
