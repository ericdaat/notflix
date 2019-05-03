import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from src.recommender.recommender import Recommender
from src.tracker.tracker import Tracker
from src.web.errors import page_not_found
from src.data_interface.model import db
from config import SQLALCHEMY_DATABASE_URI


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,
                instance_relative_config=True,
                instance_path=os.path.abspath("src/api/instance"))

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # register index
    @app.route("/status")
    def status():
        return "So far so good"

    # register database
    db.init_app(app)

    # HTTP errors
    app.register_error_handler(404, page_not_found)

    # blueprints
    from src.api import recommend
    app.register_blueprint(recommend.bp)

    with app.app_context():
        # register Recommender
        app.reco = Recommender()
        # register Tracker
        app.tracker = Tracker()

    return app
