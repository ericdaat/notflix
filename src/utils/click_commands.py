import click
import json
from flask.cli import with_appcontext
from src.data_interface import model
from src.data_interface import downloader
from src.recommender import engines


@click.command("init-db")
@with_appcontext
def init_db():
    model.init()
    click.echo("Initialized the database.")


@click.command("insert-engines")
@with_appcontext
def insert_engines():
    with open("display.json", "r") as f:
        engines = json.load(f)["engines"]

    model.insert([model.Engine(**e) for e in engines])


@click.command("insert-pages")
@with_appcontext
def insert_pages():
    with open("display.json", "r") as f:
        pages = json.load(f)["pages"]

    model.insert([model.Page(**p) for p in pages])


@click.command("download-movies")
@with_appcontext
def download_movies():
    d = downloader.MovielensDownloader()
    d.download_to_file()


@click.command("insert-movies")
@with_appcontext
def insert_movies():
    d = downloader.MovielensDownloader()
    d.insert_in_db()


@click.command("train-engines")
@with_appcontext
def train_engines():
    engine_list = [
        engines.OneHotMultiInput(),
        engines.ItemBasedCF(),
        engines.TfidfGenres(),
    ]

    for engine in engine_list:
        engine.train()


@click.command("upload-engines")
@with_appcontext
def upload_engines():
    engine_list = [
        engines.OneHotMultiInput(),
        engines.ItemBasedCF(),
        engines.TfidfGenres(),
    ]

    for engine in engine_list:
        engine.upload()
