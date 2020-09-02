""" pydantic load and evaluation of the env variables """
from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "fast-api-boilerplate"
    secret: str = "verysecretkey"
    hash_algo: str = "sha256_crypt"
    db_host: Optional[str]
    db_port: Optional[str]
    db_user: Optional[str]
    db_password: Optional[str]
    db_database: Optional[str]

