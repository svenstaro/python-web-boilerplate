""" ORM models and pydantic schemas of the user table """
from pydantic import BaseModel, Field
import databases
import orm
from .db import db_uri, metadata
from typing import Optional


class UserOutput(BaseModel):
    name: Optional[str] = Field(None, title="Unique name of the user if usr exists")
    token_status: Optional[bool] = Field(None, title="State of the token: active (True) or expired (False)")


class UserInput(BaseModel):
    name: str
    password: str
    

class UserModel(BaseModel):
    name: str
    pwhash: str


class User(orm.Model):
    """ User DAO """
    __tablename__ = "users"
    __database__ = databases.Database(db_uri)
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    name = orm.String(max_length=180, unique=True, allow_null=False)
    pwhash = orm.String(max_length=360, allow_null=False)

