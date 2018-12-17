import sqlalchemy
from flask import Blueprint, current_app, abort, jsonify, request, session
from recommender.wrappers import Context
from data import db
import logging


bp = Blueprint("recommend", __name__)


@bp.route("/recommend/product/<int:product_id>", methods=("GET",))
def product(product_id):
    try:
        active_product = db.session.query(db.notflix.Product)\
                                   .filter(db.notflix.Product.id == product_id)\
                                   .one()
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)

    r = current_app.reco
    c = Context(**{"item": active_product, "page_type": request.args.get("page_type")})

    recommendations = r.recommend(context=c)

    user_id = "foo"
    current_app.tracker.store_item_viewed("history:{0}".format(user_id), active_product.id)

    return jsonify(active_product=active_product.as_dict(),
                   recommendations=recommendations)


@bp.route("/recommend/user/<user_id>", methods=("GET",))
def user(user_id):
    r = current_app.reco
    c = Context(**{"page_type": request.args.get("page_type")})

    try:
        user = db.session.query(db.User).filter(db.User.username == user_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        user = None

    if user:
        c.user = user

    recommendations = r.recommend(context=c)

    return jsonify(active_user=user_id,
                   recommendations=recommendations)


@bp.route("/recommend/generic", methods=("GET",))
def generic():
    r = current_app.reco
    c = Context(**{"page_type": request.args.get("page_type")})

    recommendations = r.recommend(context=c)

    return jsonify(recommendations=recommendations)
