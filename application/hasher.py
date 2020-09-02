""" global hasher context object """
from passlib.context import CryptContext

from application.config import Settings


hasher = CryptContext(schemes=[Settings().hash_algo], deprecated="auto")
