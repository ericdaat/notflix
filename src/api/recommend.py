import sqlalchemy
from flask import Blueprint, current_app, abort, jsonify, request

import data.db.common
from recommender.wrappers import Context
from data import db


bp = Blueprint("recommend", __name__)


@bp.route("/recommend/product/<int:product_id>", methods=("GET",))
def product(product_id):
    try:
        active_product = db.session.query(db.notflix.Product)\
                                   .filter(db.notflix.Product.id == product_id)\
                                   .one()
        genre_names = db.session.query(db.notflix.Genre.id, db.notflix.Genre.name)\
                                .filter(db.notflix.Genre.id.in_(active_product.genres))\
                                .all()
        active_product.genres = genre_names
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)

    r = current_app.reco
    c = Context(**{"item": active_product, "page_type": request.args.get("page_type")})

    try:
        user = db.session.query(data.db.common.User) \
                 .filter(data.db.common.User.username == request.args.get("user_id")) \
                 .one()
    except sqlalchemy.orm.exc.NoResultFound:
        user = None

    if user:
        c.user = user

    recommendations = r.recommend(context=c)

    current_app.tracker.store_item_viewed("history:{0}".format(request.args.get("user_id")), active_product.id)

    return jsonify(active_product=active_product.as_dict(),
                   recommendations=recommendations)


@bp.route("/recommend/user/<user_id>", methods=("GET",))
def user(user_id):
    r = current_app.reco
    c = Context(**{"page_type": request.args.get("page_type")})

    try:
        user = db.session.query(data.db.common.User).filter(data.db.common.User.username == user_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        user = None

    if user:
        c.user = user

    recommendations = r.recommend(context=c)

    return jsonify(active_user=user_id,
                   recommendations=recommendations)
