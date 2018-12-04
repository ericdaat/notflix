from flask import Blueprint, render_template, request, redirect, url_for
from data.db import Product, Session

bp = Blueprint('search', __name__)


@bp.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        return redirect((url_for('search.search', query=request.form["query"])))

    query = request.args.get("query")
    session = Session()
    products = session.query(Product) \
                      .filter(Product.name.like('%{0}%'.format(query))) \
                      .limit(50) \
                      .all()

    return render_template('search/index.html', products=products)
