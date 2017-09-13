"""Global project configuration."""
import os
from datetime import timedelta


class Config(object):
    """Generic configuration class for default options."""

    DEBUG = False
    TESTING = False
    AUTH_TOKEN_TIMEOUT = timedelta(days=30)

    # Flask-SQLAlchemy options (see http://flask-sqlalchemy.pocoo.org/2.1/config/)
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PASSLIB_SCHEMES = ["argon2"]

    CORS_ALLOW_ORIGIN = '*'
    CORS_ALLOW_METHODS = '*'
    CORS_ALLOW_HEADERS = '*'


class ProductionConfig(Config):
    """Production specific configuration."""

    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = """
        neigh6echeih4eiqueetei2ietha1raitooSahzai6ugh0jahzahm
        u2»{1³21igh1saWooshi3uxah4oongiuphiox7iephoonahkoiK9u
    """


class StagingConfig(Config):
    """Staging specific configuration."""

    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = """
        neigh6echeih4eiqueetei2ietha1raitooSahzai6ugh0jahzahm
        u2»{1³21igh1saWooshi3uxah4oongiuphiox7iephoonahkoiK9u
    """


class DevelopConfig(Config):
    """Develop specific configuration."""

    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = """
        neigh6echeih4eiqueetei2ietha1raitooSahzai6ugh0jahzahm
        u2»{1³21igh1saWooshi3uxah4oongiuphiox7iephoonahkoiK9u
    """


class TestingConfig(Config):
    """Testing specific configuration."""

    TESTING = True
    SECRET_KEY = """
        neigh6echeih4eiqueetei2ietha1raitooSahzai6ugh0jahzahm
        u2»{1³21igh1saWooshi3uxah4oongiuphiox7iephoonahkoiK9u
    """


class LocalConfig(Config):
    """Local development specific configuration."""

    SECRET_KEY = """
        neigh6echeih4eiqueetei2ietha1raitooSahzai6ugh0jahzahm
        u2»{1³21igh1saWooshi3uxah4oongiuphiox7iephoonahkoiK9u
    """
    SQLALCHEMY_ECHO = True


configs = {
    'production': ProductionConfig,
    'staging': StagingConfig,
    'develop': DevelopConfig,
    'testing': TestingConfig,
    'local': LocalConfig,
}
