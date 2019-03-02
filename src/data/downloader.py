import csv
import json
import os
import requests
import logging
import re
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from datetime import datetime
from collections import defaultdict
from sqlalchemy.sql import null

from data.db import movielens, utils, imdb
from config import DATASETS_PATH


class Downloader(ABC):
    def __init__(self):
        # API related conf
        self.api_key = self.read_api_key("../omdb.key")
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
        self.input_filepath = os.path.join(DATASETS_PATH,
                                           "movielens/ml-20m/links.csv")
        self.output_filepath = os.path.join(DATASETS_PATH,
                                            "movielens/omdb.csv")

    def download_to_file(self):
        with open(self.output_filepath, "a") as output:
            with open(os.path.join(self.input_filepath), "r", encoding="latin1") as input:

                reader = csv.reader(input, delimiter=",", quotechar="\"")
                next(reader, None)  # skip header

                for i, (id, imdb_id, _) in enumerate(reader):
                    movie_json = self.item_from_api("tt{0}".format(imdb_id))

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

                d = {"id": movie["id"],
                     "image": movie["Poster"],
                     "name": movie["Title"],
                     "genres": [genre_dict[name] for name in genres_array],
                     "description": movie["Plot"],
                     "year": datetime.strptime(movie["Released"], "%d %b %Y") if movie["Released"] != "N/A" else None,
                     "rating": movie["imdbRating"] if movie["imdbRating"] != "N/A" else None,
                     "director": movie["Director"],
                     "actors": movie["Actors"],
                     "awards": movie["Awards"],
                     "language": movie["Language"],
                     "country": movie["Country"],
                     "duration": duration}

                movies_to_insert.append(movielens.Movie(**d))

            genres = [movielens.Genre(**{"id": id, "name": name})
                      for name, id in genre_dict.items()]

            utils.insert(genres)
            utils.insert(movies_to_insert)


class IMDBDownloader(Downloader):
    def __init__(self):
        super(IMDBDownloader, self).__init__()

    def download_to_file(self):
        pass

    def insert_in_db(self):
        CHUNKSIZE = 100

        for df in pd.read_csv(os.path.join(DATASETS_PATH, "imdb/title.basics.tsv"),
                              sep="\t", chunksize=CHUNKSIZE):
            df.rename({"tconst": "id"}, axis=1, inplace=True)
            df.replace(to_replace=r"\\N", value=np.nan, inplace=True, regex=True)
            df["genres"] = df["genres"].fillna("").str.split(",")

            df.fillna(null(), inplace=True)
            utils.insert([imdb.TitleBasics(**item) for item in df.to_dict(orient="records")])
            break

        for df in pd.read_csv("imdb/title.akas.tsv", sep="\t", chunksize=CHUNKSIZE):
            df.replace(to_replace=r"\\N", value=np.nan, inplace=True, regex=True)
            df["types"] = df["types"].fillna("").str.split(",")
            df["attributes"] = df["attributes"].fillna("").str.split(",")

            df.fillna(null(), inplace=True)
            utils.insert([imdb.TitleAkas(**item) for item in df.to_dict(orient="records")])
            break

        for df in pd.read_csv("../datasets/imdb/title.crew.tsv", sep="\t", chunksize=CHUNKSIZE):
            df.rename({"tconst": "id"}, axis=1, inplace=True)
            df.replace(to_replace=r"\\N", value=np.nan, inplace=True, regex=True)
            df["directors"] = df["directors"].fillna("").str.split(",")
            df["writers"] = df["writers"].fillna("").str.split(",")

            df.fillna(null(), inplace=True)
            utils.insert([imdb.TitleCrew(**item) for item in df.to_dict(orient="records")])
            break

        for df in pd.read_csv("../datasets/imdb/title.principals.tsv", sep="\t", chunksize=CHUNKSIZE):
            df.rename({"tconst": "title_id", "nconst": "name_id"}, axis=1, inplace=True)
            df.replace(to_replace=r"\\N", value=null(), inplace=True, regex=True)

            utils.insert([imdb.TitlePrincipals(**item) for item in df.to_dict(orient="records")])
            break

        for df in pd.read_csv("../datasets/imdb/title.ratings.tsv", sep="\t", chunksize=CHUNKSIZE):
            df.rename({"tconst": "id"}, axis=1, inplace=True)
            df.replace(to_replace=r"\\N", value=null(), inplace=True, regex=True)

            utils.insert([imdb.TitleRatings(**item) for item in df.to_dict(orient="records")])
            break

        for df in pd.read_csv("../datasets/imdb/name.basics.tsv", sep="\t", chunksize=CHUNKSIZE):
            df.rename({"nconst": "id"}, axis=1, inplace=True)
            df.replace(to_replace=r"\\N", value=np.nan, inplace=True, regex=True)
            df["primaryProfession"] = df["primaryProfession"].fillna("").str.split(",")
            df["knownForTitles"] = df["knownForTitles"].fillna("").str.split(",")

            df.fillna(null(), inplace=True)
            utils.insert([imdb.NameBasics(**item) for item in df.to_dict(orient="records")])
            break
