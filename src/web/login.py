from flask import Blueprint, render_template, request, session, redirect, url_for
import logging

bp = Blueprint("login", __name__)


def valid_login(username, password):
    return all([username, password])


@bp.route("/signin", methods=("GET", "POST"))
def signin():
    if request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]

        if valid_login(username, password):
            session["username"] = username
            return redirect(url_for('home.index'))
        else:
            error = "Bad login"
            return render_template("login/signin.html", error=error)

    return render_template("login/signin.html")


@bp.route("/signup", methods=("GET", "POST"))
def signup():
    return "sure"


@bp.route("/signout", methods=("POST",))
def signout():
    session.pop("username")

    return redirect(url_for('home.index'))

