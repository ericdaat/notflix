from flask import Blueprint, render_template
from data.db import Product, Session

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    session = Session()
    products = session.query(Product)\
                      .order_by(Product.rating.desc())\
                      .limit(10)\
                      .all()

    return render_template('home/index.html',
                           products=products,
                           recommendations=None)
