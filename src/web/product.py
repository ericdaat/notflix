from flask import Blueprint, render_template, current_app
from web.db import db_session
from data_connector.models import Product
from application.templates.context import Context


bp = Blueprint('product', __name__)


@bp.route('/product/<int:product_id>', methods=('GET', 'POST'))
def index(product_id):
    active_product = db_session.query(Product)\
                               .filter(Product.id == product_id)\
                               .one()
    r = current_app.reco
    c = Context(**{'item_id': product_id})

    recommendations = r.recommend(c)

    current_app.tracker.store_item_viewed("foo", "baz")

    return render_template('product/index.html',
                           active_product=active_product,
                           recommendations=recommendations)
