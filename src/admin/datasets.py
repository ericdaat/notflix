from data import db
from data.db import notflix
from data.downloader import OMDBDownloader


def make_movielens(with_download=False):
    url = "http://www.omdbapi.com/"
    d = OMDBDownloader("admin/omdb.key", url)

    if with_download:
        d.file_to_items_from_api(input_filepath="data/datasets/movielens/ml-20m/links.csv",
                                 output_filepath="data/datasets/movielens/omdb.csv")

    d.insert_from_file_to_db(input_filepath="data/datasets/movielens/omdb.csv")


if __name__ == "__main__":
    for table in [notflix.Product, notflix.Genre]:
        table.__table__.drop(bind=db.engine, checkfirst=True)
        table.__table__.create(bind=db.engine, checkfirst=True)

    make_movielens()
