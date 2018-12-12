# NotFlix

## About
You have just met NotFlix, a free movie database and recommendation website.

This website is simply a side project, that aims at displaying a fixed dataset of movies,
and provide recommendations about other movies to watch.

NotFlix based on data from the following sources:
 * [OMDB](http://www.omdbapi.com/): The Open Movie DataBase
 * [Grouplens' MovieLens](https://grouplens.org/datasets/movielens/): 
    Datasets behind [MovieLens](https://movielens.org/) project.

## Installation

*Note: This is a work in progress*

### Pre-requisite
You need to have [Docker](https://www.docker.com/get-started) and [docker-compose](https://docs.docker.com/compose/) installed.


### Building containers

Build the required containers:

```
docker-compose build
```


### Database

Initialize the Database:

```
make init-db
```