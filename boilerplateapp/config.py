""" pydantic load and evaluation of the env variables """
from pydantic import BaseSettings, validator
from typing import Optional
import os


# Default value are set to use testing settings, with a docker-postgres
class Configuration(BaseSettings):
    secret: str = "secretsecret"
    hash_algo: Optional[str] = "argon2"
    db_host: str = "postgres"
    db_port: str = "5432"
    db_user: str = "boilerplate"
    db_password: str = "fastapiisawesome"
    db_database: str = "boilerplate"

    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'local')}"
        env_file_encoding = 'utf-8'
