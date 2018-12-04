from flask import Blueprint, current_app, abort, jsonify
from data.db import Session
from data.db import Product
import sqlalchemy
from application.helpers import Context
import logging


bp = Blueprint('recommend', __name__)


@bp.route('/recommend/product/<int:product_id>', methods=('GET', 'POST'))
def product(product_id):
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

    return jsonify(active_product=active_product.as_dict(),
                   recommendations=recommendations)
