from .engine import QueryBasedEngine
from sqlalchemy.sql.expression import func
from src.data_interface import model
from config import MAX_RECOMMENDATIONS


class UserHistory(QueryBasedEngine):
    def __init__(self):
        super(UserHistory, self).__init__()

    def compute_query(self, session, context):
        if context.history:
            recommendations = session.query(model.Movie) \
                .filter(model.Movie.id.in_(context.history)) \
                .limit(MAX_RECOMMENDATIONS) \
                .all()
        else:
            recommendations = []

        return recommendations


class TopRated(QueryBasedEngine):
    def __init__(self):
        super(TopRated, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(model.Movie)

        if context.user and context.user.favorite_genres:
            query_filter = model.Movie.genres\
                .contains(context.user.favorite_genres)
            recommendations = recommendations.filter(query_filter)

        recommendations = recommendations \
            .order_by(model.Movie.rating.desc().nullslast()) \
            .limit(MAX_RECOMMENDATIONS)\
            .all()

        return recommendations


class MostRecent(QueryBasedEngine):
    def __init__(self):
        super(MostRecent, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(model.Movie)

        if context.user and context.user.favorite_genres:
            query_filter = model.Movie.genres\
                .contains(context.user.favorite_genres)
            recommendations = recommendations.filter(query_filter)

        recommendations = recommendations\
            .order_by(model.Movie.year.desc().nullslast())\
            .limit(MAX_RECOMMENDATIONS)\
            .all()

        return recommendations


class Random(QueryBasedEngine):
    def __init__(self):
        super(Random, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(model.Movie)

        recommendations = recommendations\
            .order_by(func.random())\
            .limit(MAX_RECOMMENDATIONS)\
            .all()

        return recommendations
