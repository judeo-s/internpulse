from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from api.v1.models import Library
from flask import Flask
"""
Module that acts as base for other modules.
"""


app = Flask(__name__)
engine = create_engine("sqlite:///data/library.db")
Library.metadata.create_all(engine)
session = Session(engine)


from api.v1.routes import library_v1
"""
Register the blueprint for versioned routes
"""


app.register_blueprint(library_v1)
