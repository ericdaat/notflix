import os
import logging
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime
from sqlalchemy.dialects import postgresql
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI


db = SQLAlchemy()


def init():
    if not database_exists(SQLALCHEMY_DATABASE_URI):
        create_database(SQLALCHEMY_DATABASE_URI)
        logging.info("Created database {0}".format(os.environ["POSTGRES_DB"]))

    db.drop_all()
    db.create_all()
    db.session.commit()


def insert(to_insert):
    if isinstance(to_insert, list):
        for item in to_insert:
            db.session.add(item)
    else:
        db.session.add(to_insert)

    return db.session.commit()


class BaseTable(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Recommendation(BaseTable):
    __tablename__ = "recommendations"
    engine_name = db.Column(db.String(56), nullable=False)
    source_item_id = db.Column(db.Integer, nullable=False)
    recommended_item_id = db.Column(db.Integer, nullable=False)
    source_item_id_kind = db.Column(db.String(56), nullable=False)
    score = db.Column(db.Float, nullable=False)


class Page(BaseTable):
    __tablename__ = "pages"
    name = db.Column(db.String(56), nullable=False, unique=True)
    engines = db.Column(postgresql.ARRAY(db.String(56)))


class Engine(BaseTable):
    __tablename__ = "engines"
    type = db.Column(db.String(20), nullable=False, unique=True)
    display_name = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.Integer, nullable=False)


class User(BaseTable):
    __tablename__ = "users"
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.Binary(60), nullable=False)
    favorite_genres = db.Column(postgresql.ARRAY(db.Integer))


class Movie(BaseTable):
    __tablename__ = "movies"
    name = db.Column(db.String(256), nullable=False)
    genres = db.Column(postgresql.ARRAY(db.Integer), nullable=True)
    image = db.Column(db.String(256), nullable=True)
    description = db.Column(db.String(512), nullable=True)
    year = db.Column(db.Date, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    director = db.Column(db.String(1024), nullable=True)
    actors = db.Column(db.String(256), nullable=True)
    awards = db.Column(db.String(256), nullable=True)
    language = db.Column(db.String(256), nullable=True)
    country = db.Column(db.String(256), nullable=True)
    duration = db.Column(db.Integer, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Genre(BaseTable):
    __tablename__ = "genres"
    name = db.Column(db.String(56), nullable=False, unique=True)
