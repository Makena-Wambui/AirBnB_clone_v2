#!/usr/bin/python3

"""
Write a script that starts a Flask web application.

Routes:
/: display “Hello HBNB!”

use the option strict_slashes=False in your route definition
application must be listening on 0.0.0.0, port 5000.
"""

from flask import Flask

my_app = Flask(__name__)


@my_app.route("/", strict_slashes=False)
def hello():
    """
    Function: hello

    Returns the message 'Hello HBNB!'
    """
    return f"Hello HBNB!"


if __name__ == "__main__":
    my_app.run(host="0.0.0.0", port="5000", debug=True)
