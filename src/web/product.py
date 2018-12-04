from flask import Blueprint, render_template, current_app, abort
from data.db import Product, Session
import sqlalchemy
from application.helpers import Context


bp = Blueprint('product', __name__)


@bp.route('/product/<int:product_id>', methods=('GET', 'POST'))
def index(product_id):
    try:
        session = Session()
        active_product = session.query(Product)\
                                .filter(Product.id == product_id)\
                                .one()
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)

    r = current_app.reco
    c = Context(**{'item_id': product_id})

    recommendations = r.recommend(c)

    current_app.tracker.store_item_viewed("history:foo", active_product.id)

    return render_template('product/index.html',
                           active_product=active_product,
                           recommendations=recommendations)
