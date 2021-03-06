import sqlalchemy
from flask import (
    Blueprint, abort, jsonify, request, current_app
)

from src.recommender.wrappers import Context
from src.data_interface import model


bp = Blueprint("recommend", __name__)


@bp.route("/recommend/item/<int:item_id>", methods=("GET",))
def item(item_id):
    # Get infos on the current item
    try:
        active_item = model.Movie.query\
            .filter(model.Movie.id == item_id)\
            .one()

        genre_names = model.Genre.query\
            .with_entities(model.Genre.id, model.Genre.name)\
            .filter(model.Genre.id.in_(active_item.genres))\
            .all()

        active_item_dict = active_item.as_dict()
        active_item_dict["genres"] = genre_names

    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)

    # Prepare for recommendations
    r = current_app.reco
    c = Context(
        item=active_item,
        page_type=request.args.get("page_type")
    )

    # add browsing history
    session_id = request.args.get("session_id")
    if session_id:
        c.history = current_app.tracker.get_views_history(
            "history:{0}".format(session_id),
            n=5
        )

    # Generate recommendations
    recommendations = r.recommend(context=c)

    # Compute the response
    res = jsonify(
        active_item=active_item_dict,
        recommendations=recommendations
    )

    return res


@bp.route("/recommend/session/<session_id>", methods=("GET",))
def session_recommendations(session_id):
    r = current_app.reco
    c = Context(
        page_type=request.args.get("page_type")
    )

    c.history = current_app.tracker.get_views_history(
        "history:{0}".format(session_id),
        n=5
    )

    recommendations = r.recommend(context=c)

    if c.history and c.page_type in {"you", "home"}:
        for item_id in c.history:
            active_item = model.Movie.query\
                .filter(model.Movie.id == item_id)\
                .one()

            c.item = active_item
            recommendations.append(
                r.recommend(
                    context=c,
                    restrict_to_engines=["OneHotMultiInput"])[0]
            )

    res = jsonify(
        session_id=session_id,
        recommendations=recommendations
    )

    return res



@bp.route("/recommend/user/<user_id>", methods=("GET",))
def user(user_id):
    r = current_app.reco
    c = Context(
        page_type=request.args.get("page_type")
    )

    try:
        user = model.User.query\
            .filter(model.User.username == user_id)\
            .one()
    except sqlalchemy.orm.exc.NoResultFound:
        user = None

    if user:
        c.user = user

        c.history = current_app.tracker.get_views_history(
            "history:{0}".format(user.username),
            n=3
        )

    recommendations = r.recommend(context=c)

    if c.history and c.page_type == "you":
        for item_id in c.history:
            active_item = model.Movie.query\
                .filter(model.Movie.id == item_id)\
                .one()

            c.item = active_item
            recommendations.append(
                r.recommend(
                    context=c,
                    restrict_to_engines=["OneHotMultiInput"])[0]
            )

    res = jsonify(
        active_user=user_id,
        recommendations=recommendations
    )

    return res
