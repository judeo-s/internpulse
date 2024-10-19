from api import app
"""
A module to handle all http requests to the Flask application
"""


@app.route('/')
def hello():
    return 'Hello, World!'
