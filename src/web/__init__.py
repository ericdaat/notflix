import os
import uuid
import logging
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, render_template, session
from src.data_interface.model import db
from src.utils import click_commands
from src.web.errors import page_not_found
from src.tracker.tracker import Tracker
from config import SQLALCHEMY_DATABASE_URI


def create_app():
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
        instance_path=os.path.abspath("src/web/instance")
    )

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

    @app.route("/about")
    def about():
        return render_template("about/index.html")

    # register database
    db.init_app(app)

    # register click commands
    app.cli.add_command(click_commands.init_db)
    app.cli.add_command(click_commands.insert_engines)
    app.cli.add_command(click_commands.insert_pages)
    app.cli.add_command(click_commands.download_movies)
    app.cli.add_command(click_commands.insert_movies)
    app.cli.add_command(click_commands.train_engines)
    app.cli.add_command(click_commands.upload_engines)

    @app.before_request
    def assign_session_id():
        if "uid" not in session:
            session["uid"] = uuid.uuid4().hex
            session.modified = True
            logging.debug("Assigned session_id {session_id}"
                          .format(session_id=session["uid"]))

    # HTTP errors
    app.register_error_handler(404, page_not_found)

    # blueprints
    from src.web import home, item, genres, search
    app.register_blueprint(home.bp)
    app.register_blueprint(item.bp)
    app.register_blueprint(genres.bp)
    app.register_blueprint(search.bp)
    # app.register_blueprint(you.bp)
    # app.register_blueprint(login.bp)

    app.add_url_rule("/", endpoint="index")

    with app.app_context():
        app.tracker = Tracker()

    return app
