from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from elasticsearch import Elasticsearch

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    # Config init
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Flask extension init
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # Custom init
    app.elasticsearch = Elasticsearch(
        [app.config["ELASTICSEARCH_URL"]], retry_on_timeout=True
    )

    # Register application (routing etc.)
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
