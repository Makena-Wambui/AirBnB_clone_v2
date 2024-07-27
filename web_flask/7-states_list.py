#!/usr/bin/python3
"""
Script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.strict_slashes = False


@app.teardown_appcontext
def close_db(self):
    """
    Remove current SQLAlchemy Session
    """
    storage.close()


@app.route('/states_list')
def list_of_states():
    """
    Displays all states present in DBStorage
    """
    return render_template('7-states_list.html',
                           state=storage.all(State).values())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
