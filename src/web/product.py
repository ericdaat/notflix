import requests
from flask import Blueprint, render_template, abort

bp = Blueprint('product', __name__)


@bp.route('/product/<int:product_id>', methods=('GET', 'POST'))
def index(product_id):
    res = requests.get("http://api:5000/recommend/product/{0}".format(product_id))

    if res.status_code != 200:
        abort(res.status_code)

    res_json = res.json()

    active_product = res_json["active_product"]
    recommendations = res_json["recommendations"]

    return render_template('product/index.html',
                           active_product=active_product,
                           recommendations=recommendations)
