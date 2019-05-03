from flask import Blueprint, render_template
from src.data_interface import model

bp = Blueprint("genres", __name__)


@bp.route("/genres", methods=("GET",))
def index():
    genres = model.Genre.query.all()

    return render_template("genres/genres.html", genres=genres)


@bp.route("/genres/<int:genre>", methods=("GET",))
def genre(genre):
    items = model.Movie.query\
        .filter(model.Movie.genres.contains([genre]))\
        .paginate(0, 50, error_out=False)\
        .items

    genre = model.Genre.query\
        .with_entities(model.Genre.id, model.Genre.name)\
        .filter(model.Genre.id == genre)\
        .one()

    return render_template("genres/genre.html", items=items, genre=genre)
