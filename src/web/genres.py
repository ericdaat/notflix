from flask import Blueprint, render_template
from src.data.db import db_scoped_session, movielens

bp = Blueprint("genres", __name__)


@bp.route("/genres", methods=("GET",))
def index():
    genres = db_scoped_session.query(movielens.Genre).all()

    return render_template("genres/genres.html", genres=genres)


@bp.route("/genres/<int:genre>", methods=("GET",))
def genre(genre):
    items = db_scoped_session\
        .query(movielens.Movie)\
        .filter(movielens.Movie.genres.contains([genre]))\
        .limit(50)\
        .all()

    genre = db_scoped_session\
        .query(movielens.Genre.id, movielens.Genre.name) \
        .filter(movielens.Genre.id == genre) \
        .one()

    return render_template("genres/genre.html", items=items, genre=genre)
