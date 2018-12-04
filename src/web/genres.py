from flask import Blueprint, render_template
from data.db import Product, Genre, Session

bp = Blueprint('genres', __name__)


@bp.route('/genres', methods=('GET',))
def index():
    session = Session()
    genres = session.query(Genre).all()

    return render_template('genres/genres.html', genres=genres)


@bp.route('/genres/<genre>', methods=('GET',))
def genre(genre):
    session = Session()
    products = session.query(Product)\
                      .filter(Product.genres.like("%{0}%".format(genre)))\
                      .limit(50)\
                      .all()

    return render_template('genres/genre.html', products=products)
