from flask import Blueprint, render_template, current_app
from application.helpers import Context


bp = Blueprint('for_you', __name__)


@bp.route('/for_you')
def index():
    views_history = current_app.tracker.get_views_history("foo", 3)

    r = current_app.reco
    recommendations = []

    for item_id in views_history:
        c = Context(**{'item_id': item_id})
        recommendations.append(r.recommend(c))

    return render_template('for_you/index.html',
                           recommendations=recommendations)
