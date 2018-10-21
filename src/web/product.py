from flask import Blueprint, render_template
from web.db import db_session
from data_connector.models import Product


bp = Blueprint('product', __name__)


@bp.route('/product/<int:product_id>', methods=('GET', 'POST'))
def index(product_id):
    active_product = db_session.query(Product)\
                               .filter(Product.id == product_id)\
                               .one()
    recommended_products = db_session.query(Product).limit(3).all()

    return render_template('product/index.html',
                           active_product=active_product,
                           recommended_products=recommended_products)
