import csv
import json
import os
import requests
import re
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from collections import defaultdict

from src.data.model import movielens, utils
from config import DATASETS_PATH


class Downloader(ABC):
    def __init__(self):
        # API related conf
        self.api_key = self.read_api_key("omdb.key")
        self.url = "http://private.omdbapi.com/"

    @abstractmethod
    def download_to_file(self):
        pass

    @abstractmethod
    def insert_in_db(self):
        pass

    def read_api_key(self, key_filepath):
        with open(key_filepath, "r") as f:
            api_key = f.read().strip()

        return api_key

    def item_from_api(self, id):
        params = {"i": "{0}".format(id), "apikey": self.api_key}
        movie_json = requests.get(url=self.url, params=params).json()

        return movie_json


class MovielensDownloader(Downloader):
    def __init__(self):
        super(MovielensDownloader, self).__init__()
        self.input_filepath = os.path.join(
            DATASETS_PATH,
            "movielens/ml-20m/links.csv"
        )

        self.output_filepath = os.path.join(
            DATASETS_PATH,
            "movielens/omdb.csv"
        )

    def download_to_file(self):
        with open(self.output_filepath, "a") as output:
            with open(self.input_filepath, "r", encoding="latin1") as input:

                reader = csv.reader(input, delimiter=",", quotechar="\"")
                next(reader, None)  # skip header

                for i, (id, imdb_id, _) in enumerate(reader):
                    try:
                        movie_json = self.item_from_api("tt{0}".format(imdb_id))
                    except json.decoder.JSONDecodeError:
                        logging.error("can't get item from API")
                        continue

                    if eval(movie_json["Response"]):
                        movie_json["id"] = id
                        output.write(json.dumps(movie_json) + "\n")
                        logging.info("got movie {0}".format(imdb_id))
                    else:
                        logging.error("failed for movie {0}".format(imdb_id))

    def insert_in_db(self):
        with open(self.output_filepath, "r") as f:
            movies_to_insert = []
            genre_dict = defaultdict(int)

            for line in f.readlines():
                movie = json.loads(line)

                if movie["id"] == "movieId":
                    continue

                # duration
                if re.match(pattern=r"[1-9]\sh", string=movie["Runtime"]):
                    duration = int(movie["Runtime"].split(" h")[0]) * 60
                elif re.match(pattern=r"[0-9]+\smin", string=movie["Runtime"]):
                    duration = int(movie["Runtime"].split(" min")[0])
                else:
                    duration = None

                # genres
                genres_array = movie["Genre"].replace(" ", "").split(",")
                for genre in genres_array:
                    if genre not in genre_dict:
                        genre_dict[genre] = len(genre_dict) + 1

                # fix fields
                year = datetime.strptime(movie["Released"], "%d %b %Y") \
                    if movie["Released"] != "N/A" else None

                rating = movie["imdbRating"] \
                    if movie["imdbRating"] != "N/A" else None

                d = {
                    "id": movie["id"],
                    "image": movie["Poster"],
                    "name": movie["Title"],
                    "genres": [genre_dict[name] for name in genres_array],
                    "description": movie["Plot"],
                    "year": year,
                    "rating": rating,
                    "director": movie["Director"],
                    "actors": movie["Actors"],
                    "awards": movie["Awards"],
                    "language": movie["Language"],
                    "country": movie["Country"],
                    "duration": duration
                }

                movies_to_insert.append(movielens.Movie(**d))

            genres = [movielens.Genre(**{"id": id, "name": name})
                      for name, id in genre_dict.items()]

            utils.insert(genres)
            utils.insert(movies_to_insert)

            logging.info("inserted {0} movies".format(len(movies_to_insert)))
            logging.info("inserted {0} genres".format(len(genres)))
