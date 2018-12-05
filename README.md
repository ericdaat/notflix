# NotFlix

## About
You have just met NotFlix, a free movie database and recommendation website.

This website is simply a side project, that aims at displaying a fixed dataset of movies,
and provide recommendations about other movies to watch.

NotFlix based on data from the following sources:
 * [OMDB](http://www.omdbapi.com/): The Open Movie DataBase
 * [Grouplens' MovieLens](https://grouplens.org/datasets/movielens/): 
    Datasets behind [MovieLens] project(https://movielens.org/).

## Installation

### On Linux
```
sudo apt-get install git;

sudo apt-get install python3;
sudo apt-get install python-pip3;

sudo apt-get install mysql-server;
sudo apt-get install libmariadbclient-dev;

sudo apt-get install redis-server;
```


### Virtual Environment
```
virtualenv venv;
source venv/bin/activate;
pip install -r requirements;
```


### Database
``` sql
GRANT ALL PRIVILEGES ON *.* TO 'notflix'@'localhost' IDENTIFIED BY 'password'
```


## Launch

``` bash
cd src;
FLASK_APP=api FLASK_DEBUG=True flask run --port 5001;
FLASK_APP=web FLASK_DEBUG=True flask run --port 5000;
```