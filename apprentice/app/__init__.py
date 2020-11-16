from config import config
from elasticsearch import Elasticsearch
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Flask extensions
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    """Initializes and configures a Flask object.

    Returns:
        The configured Flask application object.

    """
    app = Flask(__name__)

    # Config
    app.config.from_object(config[config_name])

    # Flask extension init
    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    # Custom init
    app.elasticsearch = Elasticsearch(
        [app.config["ELASTICSEARCH_URL"]], retry_on_timeout=True
    )

    # Register application blueprints (routing etc.)
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(main_blueprint)

    return app
