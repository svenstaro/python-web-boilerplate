""" pydantic load and evaluation of the env variables """
from pydantic import BaseSettings, validator
from typing import Optional
import os


# Default value are set to use testing settings, with a docker-postgres
class Configuration(BaseSettings):
    app_name: Optional[str] = "fast-api-boilerplate"
    secret: Optional[str] = "secretsecret"
    hash_algo: Optional[str] = "sha256_crypt"
    db_host: Optional[str] = "postgres"
    db_port: Optional[str] = "5432"
    db_user: Optional[str] = "boilerplate"
    db_password: Optional[str] = "fastapiisawesome"
    db_database: Optional[str] = "boilerplate"

    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'local')}"
        env_file_encoding = 'utf-8'
