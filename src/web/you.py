import requests
from flask import Blueprint, render_template, abort, request, session

from src.data_interface import model


bp = Blueprint("you", __name__)


@bp.route("/you")
def index():
    session_id = session["uid"]

    res = requests.get(
        url="http://api:8000/recommend/session/{id}".format(id=session_id),
        params={"page_type": "you"}
    )

    if res.status_code != 200:
        abort(res.status_code)

    res_json = res.json()

    recommendations = res_json["recommendations"]

    return render_template(
        "you/index.html",
        recommendations=recommendations
    )


@bp.route("/you/taste", methods=("GET", "POST"))
def taste():
    if request.method == "POST":
        form_data = request.form.to_dict(flat=False)
        user_genres = form_data.get("genre") or []

        model.User.query\
            .filter_by(username=session.get("username"))\
            .update({"favorite_genres": map(int, user_genres)})

    genres = model.Genre.query.all()
    user_genres = model.User.query\
        .with_entities(model.User.favorite_genres)\
        .filter(model.User.username == session["username"])\
        .one()[0]

    return render_template(
        "you/taste.html",
        genres=genres,
        user_genres=user_genres
    )
