""" ORM models and pydantic models for the user access tokens """
from tortoise import Model
from tortoise import fields
from pydantic import BaseModel


class UserTokens(Model):
    id = fields.IntField(pk=True)
    usr_id = fields.ForeignKeyField('models.Users')
    token_id = fields.CharField(max_length=120, unique=True)
    expiry = fields.DatetimeField()
    access_origin = fields.CharField(max_length=360)

    def __repr__(self):
        return f"{self.usr_id}: {expiry} {access_origin}"

