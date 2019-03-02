# NotFlix

[![Documentation Status](https://readthedocs.org/projects/notflix/badge/?version=latest)](https://notflix.readthedocs.io/en/latest/?badge=latest)
[![CircleCI](https://circleci.com/gh/ericdaat/notflix.svg?style=svg)](https://circleci.com/gh/ericdaat/notflix)

## About

You have just met NotFlix, a free movie database and recommendation website.

This website is simply a side project, that aims at displaying a fixed dataset of movies,
and provide recommendations about other movies to watch.

NotFlix based on data from the following sources:

* [OMDB](http://www.omdbapi.com/): The Open Movie DataBase
* [Grouplens' MovieLens](https://grouplens.org/datasets/movielens/):
    Datasets behind [MovieLens](https://movielens.org/) project.

## Installation

*Note: This is a work in progress.*

You need to have [Docker](https://www.docker.com/get-started) and [docker-compose](https://docs.docker.com/compose/) installed.

Then, run:

``` text
make install;
make init-db;
```

## Running

``` text
make start;
```

The following calls should work:

* Web: `localhost:5000/status`
* API: `localhost:5001/status`