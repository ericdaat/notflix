from flask import Blueprint, render_template
from web.db import db_session
from data.db import Product, Genre


bp = Blueprint('genres', __name__)


@bp.route('/genres', methods=('GET',))
def index():
    genres = db_session.query(Genre).all()

    return render_template('genres/genres.html', genres=genres)


@bp.route('/genres/<genre>', methods=('GET',))
def genre(genre):
    # TODO: protect from SQL injection
    products = db_session.query(Product)\
                         .filter(Product.genres.like("%{0}%".format(genre)))\
                         .limit(50)\
                         .all()

    return render_template('genres/genre.html', products=products)
