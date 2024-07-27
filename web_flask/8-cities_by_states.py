#!/usr/bin/python3
"""
Write a script that starts a Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
You must use storage for fetching data from the storage engine
    (FileStorage or DBStorage) =>
    from models import storage and storage.all(...)
To load all cities of a State:
If your storage engine is DBStorage, you must use cities relationship
Otherwise, use the public getter method cities
After each request you must remove the current SQLAlchemy Session:
    Declare a method to handle @app.teardown_appcontext
    Call in this method storage.close()
Routes:
/cities_by_states: display a HTML page: (inside the tag BODY)
H1 tag: “States”
UL tag: with the list of all State objects sorted by name (
LI tag: description of one State: <state.id>: <B><state.name></B> + UL tag:
    with the list of City objects linked to the State sorted by name (A->Z)
LI tag: description of one City: <city.id>: <B><city.name></B>
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


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


@app.route('/cities_by_states')
def cities_by_states():
    """
    Displays all cities in a state present in DBStorage
    """
    return render_template('8-cities_by_states.html',
                           state=storage.all(State).values())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
