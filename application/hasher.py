""" global hasher context object """
from passlib.context import CryptContext
from application.storage.user import UserInput, UserModel
from application.config import Configuration


hasher = CryptContext(schemes=[Configuration().hash_algo], deprecated="auto")


# TODO: orm does not play well with __init__ method
# sowe I have to use external functionality to create hash, which is a bit less secure than having it in constructor

def get_hash(usr: UserInput) -> str:
    return str(hasher.hash(f"{usr.name}{usr.password}"))


def verify(target: UserModel, origin: UserInput) -> bool:
    if target.name != origin.name:
        return False
    return hasher.verify(f"{origin.name}{origin.password}", target.pwhash)

