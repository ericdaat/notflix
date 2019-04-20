import requests
from flask import Blueprint, render_template, abort, session

bp = Blueprint("item", __name__)


@bp.route("/item/<int:item_id>", methods=("GET", "POST"))
def index(item_id):
    res = requests.get(
        url="http://api:8000/recommend/item/{0}".format(item_id),
        params={"page_type": "item", "user_id": session.get("username")}
    )

    if res.status_code != 200:
        abort(res.status_code)

    res_json = res.json()

    active_item = res_json["active_item"]
    recommendations = res_json["recommendations"]

    return render_template(
        "item/index.html",
        active_item=active_item,
        recommendations=recommendations
    )
