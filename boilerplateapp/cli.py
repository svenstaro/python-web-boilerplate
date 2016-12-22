import click
import urllib.parse
from flask import url_for
from sqlalchemy_utils.functions import database_exists, create_database, drop_database

from boilerplateapp.extensions import db
from boilerplateapp.models.user import User


def register_cli(app):
    @app.cli.command()
    def url_map():
        """Print the URL map"""

        output = []
        for rule in app.url_map.iter_rules():

            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
            output.append(line)

        for line in sorted(output):
            click.echo(line)

    @app.cli.command()
    def initdb():
        """Initialize the database

        This will drop and recreate the actual database if it already exists.
        The database name from the `SQLALCHEMY_DATABASE_URI` environment
        variable is used for this.
        """

        # If there is an existing DB, make sure to drop it and start completely fresh.
        db_url = db.engine.url
        if database_exists(db_url):
            drop_database(db_url)
        create_database(db_url)

        db.create_all()

        user = User("test@example.com", "test")
        db.session.add(user)
        db.session.commit()
