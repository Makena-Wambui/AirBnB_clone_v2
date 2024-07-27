#!/usr/bin/python3

"""
Write a script that starts a Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
use storage for fetching data from the storage engine, that is:
    (FileStorage or DBStorage)
    from models import storage and storage.all(...)

After each request you must remove the current SQLAlchemy Session:
Declare a method to handle @app.teardown_appcontext
Call in this method storage.close()

Routes:
/states_list: display a HTML page: (inside the tag BODY)
H1 tag: “States”
UL tag: with the list of all State objects present in DBStorage(sort)
LI tag: description of one State: <state.id>: <B><state.name></B>
You must use the option strict_slashes=False in your route definition
"""

from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """
    Func: states_list

    Displays an HTML page with a list of all State objects.

    States are sorted by name.

    Displayed as: <state_id>: <state_name>
    """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
