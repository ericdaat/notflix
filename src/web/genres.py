from flask import Blueprint, render_template
from src.data_interface import model, db_scoped_session

bp = Blueprint("genres", __name__)


@bp.route("/genres", methods=("GET",))
def index():
    genres = db_scoped_session.query(model.Genre).all()

    return render_template("genres/genres.html", genres=genres)


@bp.route("/genres/<int:genre>", methods=("GET",))
def genre(genre):
    items = db_scoped_session\
        .query(model.Movie)\
        .filter(model.Movie.genres.contains([genre]))\
        .limit(50)\
        .all()

    genre = db_scoped_session\
        .query(model.Genre.id, model.Genre.name) \
        .filter(model.Genre.id == genre) \
        .one()

    return render_template("genres/genre.html", items=items, genre=genre)
