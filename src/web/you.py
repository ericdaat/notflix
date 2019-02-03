import requests
from flask import Blueprint, render_template, abort, request, session

import data.db.common
from data import db
from data.db import movielens


bp = Blueprint('you', __name__)


@bp.route('/you')
def index():
    res = requests.get(url="http://api:5000/recommend/user/{0}".format(session.get("username")),
                       params={"page_type": "you"})

    if res.status_code != 200:
        abort(res.status_code)

    res_json = res.json()

    recommendations = res_json["recommendations"]

    return render_template('you/index.html',
                           recommendations=recommendations)


@bp.route("/you/taste", methods=("GET", "POST"))
def taste():
    if request.method == "POST":
        form_data = request.form.to_dict(flat=False)
        user_genres = form_data.get("genre") or []

        db.db_scoped_session.query(data.db.common.User)\
                  .filter(data.db.common.User.username == session.get("username"))\
                  .update({"favorite_genres": map(int, user_genres)})

        db.db_scoped_session.commit()

    genres = db.db_scoped_session.query(movielens.Genre).all()
    user_genres = db.db_scoped_session.query(data.db.common.User.favorite_genres)\
                            .filter(data.db.common.User.username == session["username"])\
                            .one()[0]

    return render_template("you/taste.html",
                           genres=genres,
                           user_genres=user_genres)

