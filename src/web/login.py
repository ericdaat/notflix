import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from flask import (
    Blueprint, render_template, request, session, redirect, url_for
)

from src.data.db import common, utils, db_scoped_session


bp = Blueprint("login", __name__)


def valid_signin(username, password):
    is_valid = False
    try:
        hashed_password = db_scoped_session\
            .query(common.User.password)\
            .filter(common.User.username == username)\
            .one()[0]
    except NoResultFound:
        return is_valid

    if bcrypt.checkpw(password.encode("utf8"), hashed_password):
        is_valid = True

    return is_valid


def valid_signup(username, password):
    return all([username, password])


@bp.route("/signin", methods=("GET", "POST"))
def signin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if valid_signin(username, password):
            session["username"] = username
            return redirect(url_for('home.index'))
        else:
            error = "Bad login"
            return render_template("login/signin.html", error=error)

    return render_template("login/signin.html")


@bp.route("/signup", methods=("GET", "POST"))
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if valid_signup(username, password):
            hashed_password = bcrypt.hashpw(
                password.encode("utf8"),
                bcrypt.gensalt()
            )
            user = common.User(
                username=username,
                password=hashed_password
            )
            utils.insert(user)

            return redirect(url_for('login.signin'))

    return render_template("login/signup.html")


@bp.route("/signout", methods=("POST",))
def signout():
    session.pop("username")

    return redirect(url_for('home.index'))
