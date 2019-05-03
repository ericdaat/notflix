from src.data_interface import model
from src.data_interface import downloader
from src.recommender import engines


def insert_engines():
    engines = [
        {
            "type": "OneHotMultiInput",
            "display_name": "Similar to {0}",
            "priority": 1
        },
        {
            "type": "ItemBasedCF",
            "display_name": "People also liked",
            "priority": 2
        },
        {
            "type": "TfidfGenres",
            "display_name": "Based on the same genres",
            "priority": 3
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
        {
            "type": "Random",
            "display_name": "Random Selection",
            "priority": 10
        },
    ]

    model.insert([model.Engine(**e) for e in engines])


def insert_pages():
    pages = [
        {
            "name": "home",
            "engines": ["TopRated", "MostRecent", "UserHistory", "Random"]
        },
        {
            "name": "item",
            "engines": ["OneHotMultiInput", "ItemBasedCF", "TfidfGenres"]
        }
    ]

    model.insert([model.Page(**p) for p in pages])


if __name__ == "__main__":
    d = downloader.MovielensDownloader()
    # d.download_to_file()
    # d.insert_in_db()

    insert_engines()
    insert_pages()

    # engines = [
    #     engines.OneHotMultiInput(),
    #     engines.ItemBasedCF(),
    #     engines.TfidfGenres(),
    # ]

    # for e in engines:
    #     e.train()
    #     e.upload()
