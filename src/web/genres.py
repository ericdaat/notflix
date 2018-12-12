from flask import Blueprint, render_template
from data.db import Product, Genre, session

bp = Blueprint('genres', __name__)


@bp.route('/genres', methods=('GET',))
def index():
    genres = session.query(Genre).all()

    return render_template('genres/genres.html', genres=genres)


@bp.route('/genres/<genre>', methods=('GET',))
def genre(genre):
    products = session.query(Product)\
                      .filter(Product.genres.ilike("%{0}%".format(genre)))\
                      .limit(50)\
                      .all()

    return render_template('genres/genre.html', products=products)
