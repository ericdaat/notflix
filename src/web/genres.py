from flask import Blueprint, render_template, request
from src.data_interface import model
from config import MAX_MOVIES_PER_LISTING

bp = Blueprint("genres", __name__)


@bp.route("/genres", methods=("GET",))
def index():
    genres = model.Genre.query.all()

    return render_template("genres/genres.html", genres=genres)


@bp.route("/genres/<int:genre>", methods=("GET",))
def genre(genre):
    page = request.args.get("page") or 1

    items = model.Movie.query.filter(model.Movie.genres.contains([genre]))

    items_count = items.count()

    items_on_page = items\
        .paginate(int(page), MAX_MOVIES_PER_LISTING, error_out=False)\
        .items

    genre = model.Genre.query\
        .with_entities(model.Genre.id, model.Genre.name)\
        .filter(model.Genre.id == genre)\
        .one()

    return render_template(
        "genres/genre.html",
        items=items_on_page,
        number_of_pages=(items_count // MAX_MOVIES_PER_LISTING) + 1,
        genre=genre
    )
