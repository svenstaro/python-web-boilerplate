""" connection setup """
import sqlalchemy
import orm
import databases
from application.config import Configuration


conf = Configuration()


def get_db_uri(conf: Configuration) -> str:
    """ create proper db_uri from partial data """
    if None in [conf.db_user, conf.db_password, conf.db_host, conf.db_port]:
        return "postgresql://boilerplate:fastapiisawesome@postgres:5432/boilerplate"
    return f"postgresql://{conf.db_user}:{conf.db_password}@{conf.db_host}:{conf.db_port}/{conf.db_database}"

db_uri = get_db_uri(conf)
print(db_uri)
database = databases.Database(db_uri)
metadata = sqlalchemy.MetaData()
