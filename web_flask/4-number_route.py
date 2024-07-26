#!/usr/bin/python3

"""
Write a script that starts a Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
Routes:
/: display “Hello HBNB!”
/hbnb: display “HBNB”
/c/<text>: display “C ”, followed by the value of the text variable
(replace underscore _ symbols with a space )
/python/<text>: display “Python ”, followed by the value of the text variable
(replace underscore _ symbols with a space )
The default value of text is “is cool”

/number/<n>: display “n is a number” only if n is an integer

You must use the option strict_slashes=False in your route definition
"""

from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """
    function: hello
    Prints Hello HBNB!
    """
    return f"Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Function: hbnb
    Prints HBNB
    """
    return f"HBNB"


@app.route("/c/<text>", strict_slashes=False)
# @app.route("/c", strict_slashes=False)
def c_text(text="is cool"):
    """
    Func: c_text
    Prints "C + text"
    """
    return "C {}".format(text.replace("_", " "))


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python", strict_slashes=False)
def python(text="is cool"):
    """
    Func: python
    Prints "Python + text"
    """
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>")
def number(n):
    """
    Func: number
    Prints=> n is a number only if n is an int.
    """
    return f"{n} is a number"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
