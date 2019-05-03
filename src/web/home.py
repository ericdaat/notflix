import requests
from flask import Blueprint, render_template, abort, session

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    session_id = session.get("uid")

    res = requests.get(
        url="http://api:8000/recommend/session/{id}"
            .format(id=session_id),
        params={"page_type": "home"})

    if res.status_code != 200:
        abort(res.status_code)

    res_json = res.json()
    recommendations = res_json["recommendations"]

    return render_template(
        "home/index.html",
        recommendations=recommendations
    )
