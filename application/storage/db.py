""" connection setup """
import sqlalchemy
import orm
import databases
from application.config import DBSettings


config = DBSettings()


def get_db_uri(config: DBSettings) -> str:
    """ create proper db_uri from partial data """
    # if config.all_values_are_present():
    #     return f"postgres://{config['db_user']:config['db_password']@config['db_host']:config['db_port']/config['db_database']}"
    return "postgresql://postgres:postgres@postgres:5432/boilerplate"

db_uri = get_db_uri(config)
database = databases.Database(db_uri)
metadata = sqlalchemy.MetaData()
