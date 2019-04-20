import logging
from src.data.db import common, utils
from src.data import downloader
from src.recommender import engines


def init_db():
    utils.init()
    logging.info("database initialized")


def download_data(insert_in_db=True):
    d = downloader.MovielensDownloader()
    d.download_to_file()

    if insert_in_db:
        d.insert_in_db()


def insert_engines():
    utils.insert([
        common.Engine(**{"type": "OneHotMultiInput", "display_name": "Similar to {0}", "priority": 1}),
        common.Engine(**{"type": "TopRated", "display_name": "Top rated movies", "priority": 1}),
        common.Engine(**{"type": "MostRecent", "display_name": "Uploaded recently", "priority": 2}),
        common.Engine(**{"type": "UserHistory", "display_name": "Your browsing history", "priority": 2})
    ])


def insert_pages():
    utils.insert([
        common.Page(**{"name": "home", "engines": ["TopRated", "MostRecent"]}),
        common.Page(**{"name": "item", "engines": ["OneHotMultiInput"]}),
        common.Page(**{"name": "you", "engines": ["UserHistory"]}),
    ])


if __name__ == "__main__":
    download_data(insert_in_db=True)
    insert_engines()
    insert_pages()

    e = engines.OneHotMultiInput()
    e.train()
    e.upload()
