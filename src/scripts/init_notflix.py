import logging
from src.data_interface import model
from src.data_interface import downloader
from src.recommender import engines


def init_db():
    model.init()
    logging.info("database initialized")


def download_data(insert_in_db=True):
    d = downloader.MovielensDownloader()
    d.download_to_file()

    if insert_in_db:
        d.insert_in_db()


def insert_engines():
    engines = [
        {
            "type": "OneHotMultiInput",
            "display_name": "Similar to {0}",
            "priority": 1
        },
        {
            "type": "TopRated",
            "display_name": "Top rated movies",
            "priority": 1
        },
        {
            "type": "MostRecent",
            "display_name": "Uploaded recently",
            "priority": 2
        },
        {
            "type": "UserHistory",
            "display_name": "Your browsing history",
            "priority": 2
        },
    ]

    model.insert([model.Engine(**e) for e in engines])


def insert_pages():
    pages = [
        {"name": "home", "engines": ["TopRated", "MostRecent"]},
        {"name": "item", "engines": ["OneHotMultiInput"]},
        {"name": "you", "engines": ["UserHistory"]}
    ]

    model.insert([model.Page(**p) for p in pages])


if __name__ == "__main__":
    init_db()
    download_data(insert_in_db=True)
    insert_engines()
    insert_pages()

    e = engines.OneHotMultiInput()
    e.train()
    e.upload()
