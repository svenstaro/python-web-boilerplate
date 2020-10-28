""" ORM models and pydantic models for the user access tokens """
from pydantic import BaseModel
import databases
import orm
from .db import db_uri, metadata, database
from .user import User
from datetime import timedelta
import datetime
import uuid


class UserTokens(orm.Model):
    """ access token DAO """
    __tablename__ = "token"
    __database__ = database
    __metadata__ = metadata


    id = orm.Integer(primary_key=True)
    usr = orm.ForeignKey(User)
    token = orm.String(max_length=120, unique=True)
    expiry = orm.DateTime()
    access_origin = orm.String(max_length=360)


class Token(BaseModel):
    token: str 
