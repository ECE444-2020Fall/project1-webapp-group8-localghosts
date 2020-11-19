import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base config class (for settings common to all configuration types)"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    APPRENTICE_ADMIN = os.environ.get("APPRENTICE_ADMIN")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL") or "http://localhost:9200"


class DevelopmentConfig(Config):
    """Config class for development"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


class TestingConfig(Config):
    """Config class for testing"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"


class ProductionConfig(Config):
    """Config class for production"""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
