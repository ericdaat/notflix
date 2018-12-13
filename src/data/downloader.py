import csv
import json
import os
import requests
import logging
import re
from datetime import datetime
from collections import defaultdict
from abc import abstractmethod, ABC

from data.db import notflix, insert, DB_HOST


class Downloader(ABC):
    def __init__(self, key_filepath, url):
        self.api_key = self.read_key(key_filepath)
        self.url = url

    def read_key(self, key_filepath):
        with open(key_filepath, "r") as f:
            api_key = f.read().strip()

        return api_key

    @abstractmethod
    def item_from_api(self, id):
        pass

    @abstractmethod
    def file_to_items_from_api(self, input_filepath, output_filepath):
        pass

    @abstractmethod
    def insert_from_file_to_db(self, input_filepath):
        pass


class OMDBDownloader(Downloader):
    def __init__(self, api_key, url):
        super(OMDBDownloader, self).__init__(api_key, url)

    def item_from_api(self, id):
        params = {"i": "tt{0}".format(id), "apikey": self.api_key}
        movie_json = requests.get(url=self.url, params=params).json()

        return movie_json

    def file_to_items_from_api(self, input_filepath, output_filepath):
        with open(output_filepath, "a") as output:
            with open(os.path.join(input_filepath), "r", encoding="latin1") as input:

                reader = csv.reader(input, delimiter=',', quotechar='"')
                next(reader, None)  # skip header

                for i, (id, imdb_id, _) in enumerate(reader):
                    movie_json = self.item_from_api(imdb_id)

                    if eval(movie_json["Response"]):
                        movie_json["id"] = id
                        output.write(json.dumps(movie_json) + "\n")
                    else:
                        logging.error("failed for movie index {0}".format(i))

    def insert_from_file_to_db(self, input_filepath):
        with open(input_filepath, "r") as f:
            products = []
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

                d = {"id": movie["id"],
                     "image": movie["Poster"],
                     "name": movie["Title"],
                     "genres": movie["Genre"],
                     "description": movie["Plot"],
                     "year": datetime.strptime(movie["Released"], "%d %b %Y") if movie["Released"] != "N/A" else None,
                     "rating": movie["imdbRating"] if movie["imdbRating"] != "N/A" else None,
                     "director": movie["Director"],
                     "actors": movie["Actors"],
                     "awards": movie["Awards"],
                     "language": movie["Language"],
                     "country": movie["Country"],
                     "duration": duration}

                product = notflix.Product(**d)
                products.append(product)

            genres = [notflix.Genre(**{"id": id, "name": name}) for name, id in genre_dict.items()]
            insert(genres, db_host=DB_HOST)
            insert(products, db_host=DB_HOST)
