from flask import Blueprint, current_app, abort, jsonify, request
from data.db import session
from data.db import Product
import sqlalchemy
from recommender.helpers import Context


bp = Blueprint("recommend", __name__)


@bp.route("/recommend/product/<int:product_id>", methods=("GET",))
def product(product_id):
    try:
        active_product = session.query(Product)\
                                .filter(Product.id == product_id)\
                                .one()
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)

    r = current_app.reco
    c = Context(**{"item_id": product_id, "page_type": request.args.get("page_type")})

    recommendations = r.recommend(context=c)

    user_id = "foo"
    current_app.tracker.store_item_viewed("history:{0}".format(user_id), active_product.id)

    return jsonify(active_product=active_product.as_dict(),
                   recommendations=recommendations)


@bp.route("/recommend/user/<user_id>", methods=("GET",))
def user(user_id):
    views_history = current_app.tracker.get_views_history("history:{0}".format(user_id), 3)

    r = current_app.reco
    recommendations = []

    for item_id in views_history:
        c = Context(**{"item_id": item_id, "page_type": request.args.get("page_type")})
        recommendations.append(r.recommend(context=c))

    return jsonify(active_user=user_id,
                   recommendations=recommendations)


@bp.route("/recommend/generic", methods=("GET",))
def generic():
    r = current_app.reco
    c = Context(**{"page_type": request.args.get("page_type")})
    recommendations = r.recommend(context=c)

    return jsonify(recommendations=recommendations)
