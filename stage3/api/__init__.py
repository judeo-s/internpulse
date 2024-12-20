from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from api.models import Base
"""
Module that acts as base for other modules.
"""


app = Flask(__name__)
engine = create_engine("sqlite:///shop.db")
Base.metadata.create_all(engine)
session = Session(engine)


from api.views import root
app.register_blueprint(root)

