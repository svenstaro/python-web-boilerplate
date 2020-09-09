""" ORM models and pydantic schemas of the user table """
from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel
from application.hasher import hasher


class Users(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=120, unique=True, required=True)
    pwhash = fields.CharField(max_length=360, required=True)

    def __init__(self, name: str, password: str) -> None:
        self.name = name
        self.pwhash = self.hash(name, password)

    def __repr__(self):
        return f"{self.id}: {self.name}"

    def hash(self, username: str, pwd: str) -> None:
        """ save pwd hash """
        self.pwhash = hasher.hash(f"{username}{pwd}")

    def verify(self, password: str) -> bool:
        return hasher.verify(f"{self.name}{password}", self.pwhash)


class UserInput(BaseModel):
    name: str
    password: str
    


class UserOutput(BaseModel):
    id: int
    name: str
