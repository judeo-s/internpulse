from . import app
"""
This module is for initializing the flask application.
"""


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
