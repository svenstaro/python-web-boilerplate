""" ORM models and pydantic schemas of the user table """
from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel


class Users(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=120, unique=True, required=True)
    pwhash = fields.CharField(max_length=360, required=True)

    def __repr__(self):
        return f"{self.id}: {self.name}"


class UserInput(BaseModel):
    name: str
    password: str
    


class UserOutput(BaseModel):
    id: int
    name: str
