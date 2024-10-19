from flask import Flask
from sqlalchemy import create_engine
from models import Base
"""
Module that acts as base for other modules.
"""

app = Flask(__name__)
engine = create_engine("sqlite://internpulse.db", echo=True)

