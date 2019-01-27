import sqlalchemy
from flask import Blueprint, current_app, abort, jsonify, request

from recommender.wrappers import Context
from data.db import common, notflix, session


bp = Blueprint("recommend", __name__)


@bp.route("/recommend/item/<int:item_id>", methods=("GET",))
def item(item_id):
    try:
        active_item = session.query(notflix.Movie)\
                             .filter(notflix.Movie.id == item_id)\
                             .one()
        genre_names = session.query(notflix.Genre.id, notflix.Genre.name)\
                             .filter(notflix.Genre.id.in_(active_item.genres))\
                             .all()
        active_item.genres = genre_names
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)

    r = current_app.reco
    c = Context(**{"item": active_item, "page_type": request.args.get("page_type")})

    try:
        user = session.query(common.User) \
                      .filter(common.User.username == request.args.get("user_id")) \
                      .one()
    except sqlalchemy.orm.exc.NoResultFound:
        user = None

    if user:
        c.user = user

    recommendations = r.recommend(context=c)

    current_app.tracker.store_item_viewed("history:{0}".format(request.args.get("user_id")),
                                          active_item.id)

    return jsonify(active_item=active_item.as_dict(),
                   recommendations=recommendations)


@bp.route("/recommend/user/<user_id>", methods=("GET",))
def user(user_id):
    r = current_app.reco
    c = Context(**{"page_type": request.args.get("page_type")})

    try:
        user = session.query(common.User).filter(common.User.username == user_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        user = None

    if user:
        c.user = user
        c.history = current_app.tracker.get_views_history("history:{0}".format(user.username), n=3)

    recommendations = r.recommend(context=c)

    if c.history and c.page_type == "you":
        for item_id in c.history:
            active_item = session.query(notflix.Movie) \
                                 .filter(notflix.Movie.id == item_id) \
                                 .one()

            c.item = active_item
            recommendations.append(r.recommend(context=c, restrict_to_engines=["OneHotMultiInput"])[0])

    return jsonify(active_user=user_id,
                   recommendations=recommendations)
