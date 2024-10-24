import os
from logging.config import dictConfig

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def handle_404_error(e):
    """ Error handler for 404.

        Used when abort() is called. THe custom message is provided by the
        'description=' parameter in abort().
        Args:
            HTTP 404 error

        Returns:
            JSON response with the validation error message and the 404 status
            code
        """
    return jsonify(error=str(e)), 404


# First create the db object using the SQLAlchemy constructor.
# Pass a subclass of either DeclarativeBase or DeclarativeBaseNoMeta to the
# constructor.
db = SQLAlchemy(model_class=Base)

# Create the Marshmallow instance after SQLAlchemy
ma = Marshmallow()


def create_app(test_config=None):

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers':
            {'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": "src_log.log",
                    "formatter": "default",
                },
            },
        "root": {"level": "DEBUG", "handlers": ["wsgi", "file"]},
    })

    # create the Flask app
    app = Flask(__name__, instance_relative_config=True)
    # configure the Flask app (see later notes on how to generate my own
    # SECRET_KEY)
    app.config.from_mapping(
        SECRET_KEY='Rsi0V6yieyvpC_nTkY1_lQ',
        # Set the location of the database file called paralympics.sqlite
        # which will be in the app's instance folder
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path,
                                                            'src.sqlite'))

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register the custom 404 error handler that is defined in this python file
    app.register_error_handler(401, handle_404_error)

    # Initialise Flask with the SQLAlchemy database extension
    db.init_app(app)
    # Initialise Flask-Marshmallow
    ma.init_app(app)

    # Models are defined in the models module, so you must import them before
    # calling create_all, otherwise SQLAlchemy
    # will not know about them.
    from src.models import User, Feedback, Age_group, Gender, Ethnicity, \
        Employment, Course_level, Teacher, Disability
    # Create the tables in the database
    # create_all does not update tables if they are already in the database.
    with app.app_context():
        db.create_all()

        # Add the data to the database if not already added
        from src.utils import add_data
        add_data(db)
        # Register the routes with the app in the context

        from src import routes, error_handlers

    return app
