from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from api.models import Library
from flask import Flask
"""
Module that acts as base for other modules.
"""


app = Flask(__name__)
engine = create_engine("sqlite:///library.db")
Library.metadata.create_all(engine)
session = Session(engine)

from api.routes import library
app.register_blueprint(library)