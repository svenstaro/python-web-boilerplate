""" ORM models and pydantic models for the user access tokens """
from tortoise import Model
from tortoise import fields
from pydantic import BaseModel
from datetime import timedelta
import datetime
import uuid


class UserTokens(Model):
    id = fields.IntField(pk=True)
    usr_id = fields.ForeignKeyField('models.Users')
    token_id = fields.CharField(max_length=120, unique=True)
    expiry = fields.DatetimeField()
    access_origin = fields.CharField(max_length=360)

    def __init__(self, usr_id: int, access_origin: str):
        
        self.usr_id = usr_id
        self.access_origin = access_origin
        self.expiry = datetime.datetime.now() + timedelta(days=7)
        self.token_id = str(uuid.uuid4())

    def __repr__(self):
        return f"{self.usr_id}: {expiry} {access_origin}"


class Token(BaseModel):
    token_id: str 
    access_origin: str
