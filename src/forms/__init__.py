import sqlite3
from flask import g, Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, validators


# Normally don't store your database right here
# read https://12factor.net/config
DATABASE = "./database.db"

app = Flask(__name__)


class PersonForm(Form):
    name = StringField("Name", [validators.InputRequired()])


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    people = query_db("SELECT * FROM people")

    return render_template("index.html", people=people)


@app.route("/person", methods=["GET", "POST"])
def add_person():
    if request.method == "POST":
        form = PersonForm(request.form)
        if form.validate():
            query_db(f"INSERT INTO people (name) VALUES ('{form.name.data}')")
            query_db("COMMIT")
            return redirect(url_for("index"))
    else:
        form = PersonForm()
    return render_template("add-person.html", form=form)


@app.route("/person/<person_name>", methods=["GET", "POST"])
def edit_person(person_name):
    # Get user from query parameter (usually this would be an ID
    # like an integer or uuid, but here we use the string name
    if request.method == "POST":
        form = PersonForm(request.form)
        if form.validate():
            query_db(
                f"UPDATE people SET name = '{form.name.data}' WHERE name = '{person_name}'"
            )
            query_db("COMMIT")
            return redirect(url_for("index"))
    else:
        person = query_db(
            f"SELECT * FROM people WHERE name ='{person_name}'", one=True
        )  # noqa: E501

        # Convert the response into a dict (if you're using
        # SqlAlchemy you don't need to do this.
        person = dict(person)
        form = PersonForm(data=person)
    return render_template("edit-person.html", form=form)


@app.route("/person/<person_name>/delete", methods=["GET"])
def delete_person(person_name):
    query_db(f"DELETE FROM people WHERE name='{person_name}'")
    query_db("COMMIT")
    return redirect(url_for("index"))


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def make_dicts(cursor, row):
    """
    https://flask.palletsprojects.com/en/3.0.x/patterns/sqlite3/#easy-querying
    """
    return dict(
        (cursor.description[idx][0], value) for idx, value in enumerate(row)
    )  # noqa: E501


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
