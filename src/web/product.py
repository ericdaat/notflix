import requests
from flask import Blueprint, render_template, abort, session

bp = Blueprint('product', __name__)


@bp.route('/product/<int:product_id>', methods=('GET', 'POST'))
def index(product_id):
    res = requests.get(url="http://api:5000/recommend/product/{0}".format(product_id),
                       params={"page_type": "product",
                               "user_id": session.get("username")})

    if res.status_code != 200:
        abort(res.status_code)

    res_json = res.json()

    active_product = res_json["active_product"]
    recommendations = res_json["recommendations"]

    return render_template('product/index.html',
                           active_product=active_product,
                           recommendations=recommendations)
