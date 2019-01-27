from recommender.engines.engine import QueryBasedEngine, OfflineEngine, Engine
from config import MAX_RECOMMENDATIONS
from data.db import notflix


class SameGenres(QueryBasedEngine):
    def __init__(self):
        super(SameGenres, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(notflix.Movie)\
                           .filter(notflix.Movie.genres.contains([g[0] for g in context.item.genres]))\
                           .filter(notflix.Movie.id != context.item.id) \
                           .limit(MAX_RECOMMENDATIONS).all()

        return recommendations


class OneHotMultiInput(OfflineEngine):
    def __init__(self):
        super(OneHotMultiInput, self).__init__()

    def train(self):
        pass


class TfidfGenres(OfflineEngine):
    def __init__(self):
        super(TfidfGenres, self).__init__()

    def train(self):
        pass


class TopRated(QueryBasedEngine):
    def __init__(self):
        super(TopRated, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(notflix.Movie)

        if context.user and context.user.favorite_genres:
            recommendations = recommendations.filter(notflix.Movie.genres.contains(context.user.favorite_genres))

        recommendations = recommendations \
            .order_by(notflix.Movie.rating.desc().nullslast()) \
            .limit(MAX_RECOMMENDATIONS).all()

        return recommendations


class MostRecent(QueryBasedEngine):
    def __init__(self):
        super(MostRecent, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(notflix.Movie)

        if context.user and context.user.favorite_genres:
            recommendations = recommendations.filter(notflix.Movie.genres.contains(context.user.favorite_genres))

        recommendations = recommendations.order_by(notflix.Movie.year.desc().nullslast()) \
                                         .limit(MAX_RECOMMENDATIONS).all()

        return recommendations
