import logging
from data.db import common, utils
from data.datasets import downloader
from recommender import engines


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Drop and create all tables
    utils.init()

    d = downloader.MovielensDownloader()
    d.insert_in_db()

    # insert engines
    utils.insert([
        common.Engine(**{"type": "OneHotMultiInput", "display_name": "Similar to {0}", "priority": 1}),
        common.Engine(**{"type": "TopRated", "display_name": "Top rated movies", "priority": 1}),
        common.Engine(**{"type": "MostRecent", "display_name": "Uploaded recently", "priority": 2}),
        common.Engine(**{"type": "UserHistory", "display_name": "Your browsing history", "priority": 2})
    ])

    # insert pages
    utils.insert([
        common.Page(**{"name": "home", "engines": ["TopRated", "MostRecent"]}),
        common.Page(**{"name": "item", "engines": ["OneHotMultiInput"]}),
        common.Page(**{"name": "you", "engines": ["UserHistory"]}),
    ])

    # train & upload engines
    engines.OneHotMultiInput().upload()
