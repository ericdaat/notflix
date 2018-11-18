import os

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from application.recommender import Recommender
from .db import db_session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # register index
    @app.route('/status')
    def index():
        return 'So far so good'

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # blueprints
    from web import home, product, genres, search
    app.register_blueprint(home.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(genres.bp)
    app.register_blueprint(search.bp)

    app.add_url_rule('/', endpoint='index')

    app.reco = Recommender()

    return app
