import os
from data.db import common, utils, notflix, DB_HOST
from data.downloader import OMDBDownloader
from recommender import engines


if __name__ == "__main__":
    # Drop and create all tables
    utils.init(db_host=DB_HOST)

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

    # insert engines
    utils.insert([
        notflix.Engine(**{"type": "TfidfGenres", "display_name": "Similar to {0}", "priority": 1}),
        notflix.Engine(**{"type": "TopRated", "display_name": "Top rated movies", "priority": 1}),
        notflix.Engine(**{"type": "MostRecent", "display_name": "Recent movies", "priority": 2}),
        notflix.Engine(**{"type": "UserHistory", "display_name": "Your browsing history", "priority": 2})
    ],
        db_host=DB_HOST
    )

    # insert pages
    utils.insert([
        common.Page(**{"name": "home", "engines": ["TopRated", "MostRecent"]}),
        common.Page(**{"name": "product", "engines": ["TfidfGenres"]}),
        common.Page(**{"name": "you", "engines": ["UserHistory"]}),
    ],
        db_host=DB_HOST
    )

    # train & upload engines
    engines.TfidfGenres().upload()
