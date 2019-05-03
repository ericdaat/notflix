from flask import Blueprint, render_template, request, redirect, url_for
from src.data_interface import model

bp = Blueprint("search", __name__)


@bp.route("/search", methods=("GET", "POST"))
def search():
    if request.method == "POST":
        return redirect(
            url_for("search.search", query=request.form["query"])
        )

    query = request.args.get("query")
    items = model.Movie.query\
        .filter(model.Movie.name.ilike("%{0}%".format(query))) \
        .paginate(0, 50, error_out=False)\
        .items

    return render_template("search/index.html", items=items)
