""" ORM models and pydantic schemas of the user table """
from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel
from application.hasher import hasher


class UserInput(BaseModel):
    name: str
    password: str
    

class UserOutput(BaseModel):
    id: int
    name: str


class Users(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=120, unique=True, required=True)
    pwhash = fields.CharField(max_length=360, required=True)

    def __init__(self, usr: UserInput) -> None:
        # TODO: not sure why these are not set by default
        self._partial = False
        self._saved_in_db = False
        self._custom_generated_pk = False

        self.name = usr.name
        self.pwhash = self.hash(usr)

    def __repr__(self):
        return f"{self.id}: {self.name}"

    def hash(self, usr: UserInput) -> str:
        """ prepare pwd hash """
        return hasher.hash(f"{usr.name}{usr.password}")

    def verify(self, password: str) -> bool:
        return hasher.verify(f"{self.name}{password}", self.pwhash)


