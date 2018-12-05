from flask import Blueprint, render_template, abort
import requests


bp = Blueprint('you', __name__)


@bp.route('/you')
def index():
    user_id = "foo"
    res = requests.get("http://api:5000/recommend/user/{0}".format(user_id))

    if res.status_code != 200:
        abort(res.status_code)

    res_json = res.json()

    recommendations = res_json["recommendations"]

    return render_template('you/index.html',
                           recommendations=recommendations)
