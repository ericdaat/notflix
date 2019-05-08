from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from src.data_interface import model
from config import MAX_MOVIES_PER_LISTING

bp = Blueprint("search", __name__)


@bp.route("/search", methods=("GET", "POST"))
def search():
    page = request.args.get("page") or 1

    if request.method == "POST":
        return redirect(
            url_for("search.search", query=request.form["query"])
        )

    query = request.args.get("query")
    items = model.Movie.query\
        .filter(model.Movie.name.ilike("%{0}%".format(query)))

    items_count = items.count()

    items_on_page = items\
        .paginate(int(page), MAX_MOVIES_PER_LISTING, error_out=False)\
        .items

    return render_template(
        "search/index.html",
        items=items_on_page,
        number_of_pages=(items_count // MAX_MOVIES_PER_LISTING) + 1,
    )
