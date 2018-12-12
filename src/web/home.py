import requests
from flask import Blueprint, render_template, abort

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    res = requests.get(url="http://api:5000/recommend/generic",
                       params={"page_type": "home"})

    if res.status_code != 200:
        abort(res.status_code)

    res_json = res.json()
    recommendations = res_json["recommendations"]

    return render_template('home/index.html',
                           recommendations=recommendations)
