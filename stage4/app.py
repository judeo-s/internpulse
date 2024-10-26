"""
A module to initialize a the flask application.

This module is the entry point for the application. When this module is run
directly (i.e., not imported as a module), it will initialize the Flask
application and run it in debug mode on localhost:5000.

"""
from api import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

