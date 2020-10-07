""" pydantic load and evaluation of the env variables """
from pydantic import BaseSettings, validator
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "fast-api-boilerplate"
    secret: str = "verysecretkey"


class HashSetting(BaseSettings):
    hash_algo: str = "sha256_crypt"


class DBSettings(BaseSettings):
    db_host: Optional[str]
    db_port: Optional[str]
    db_user: Optional[str]
    db_password: Optional[str]
    db_database: Optional[str]

    # @validator('db_host', 'db_port', 'db_user', 'db_password', 'db_database')
    def all_values_are_present(self) -> bool:
        if v is not None:
            return True
        return False

