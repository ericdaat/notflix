from flask import Blueprint, render_template, request, redirect, url_for
from src.data_interface import model, db_scoped_session

bp = Blueprint("search", __name__)


@bp.route("/search", methods=("GET", "POST"))
def search():
    if request.method == "POST":
        return redirect(
            url_for("search.search", query=request.form["query"])
        )

    query = request.args.get("query")
    items = db_scoped_session\
        .query(model.Movie) \
        .filter(model.Movie.name.ilike("%{0}%".format(query))) \
        .limit(50) \
        .all()

    return render_template("search/index.html", items=items)
