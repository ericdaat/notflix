import os
from data.db import DB_HOST, init
from data.downloader import OMDBDownloader


if __name__ == "__main__":
    # Drop and create all tables
    init(db_host=DB_HOST)

    # general variables
    url = "http://www.omdbapi.com/"
    d = OMDBDownloader("admin/omdb.key", url)
    dataset_path = "data/datasets/movielens/omdb.csv"

    # download dataset
    if not os.path.isfile(dataset_path):
        d.file_to_items_from_api(input_filepath="data/datasets/movielens/ml-20m/links.csv",
                                 output_filepath=dataset_path)

    # insert downloaded dataset
    d.insert_from_file_to_db(input_filepath="data/datasets/movielens/omdb.csv")


