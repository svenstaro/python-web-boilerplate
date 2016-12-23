"""This module contains various extensions which will serve as a global import location.

These extensions are instantiated here but they won't be initialized until the
factory function is called.
"""
from flask_sqlalchemy import SQLAlchemy
from boilerplateapp.helpers.passlib import Passlib


db = SQLAlchemy()
passlib = Passlib()
