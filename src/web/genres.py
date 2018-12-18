from flask import Blueprint, render_template
from data.db import session, notflix

bp = Blueprint('genres', __name__)


@bp.route('/genres', methods=('GET',))
def index():
    genres = session.query(notflix.Genre).all()

    return render_template('genres/genres.html', genres=genres)


@bp.route('/genres/<int:genre>', methods=('GET',))
def genre(genre):
    products = session.query(notflix.Product)\
                      .filter(notflix.Product.genres.contains([genre]))\
                      .limit(50)\
                      .all()
    genre = session.query(notflix.Genre.id, notflix.Genre.name) \
                   .filter(notflix.Genre.id == genre) \
                   .one()

    return render_template('genres/genre.html', products=products, genre=genre)
