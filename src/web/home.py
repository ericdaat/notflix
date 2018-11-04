from flask import Blueprint, render_template, current_app
from web.db import db_session
from data_connector.models import Product as ProductTable
from application.templates.context import Context

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    products = db_session.query(ProductTable).limit(10).all()

    views_history = current_app.tracker.get_views_history("foo", 1)

    r = current_app.reco
    recommendations = []

    for item_id in views_history:
        c = Context(**{'item_id': item_id})
        recommendations.append(r.recommend(c))

    return render_template('home/index.html',
                           products=products,
                           recommendations=recommendations)
