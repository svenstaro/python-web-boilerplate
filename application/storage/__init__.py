""" factory method to connect to connect to DBs """
from tortoise import Tortoise


async def db_init(db_url: str = "postgres://postgres:postgres@postgres:5432/boilerplate") -> Tortoise:
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["application.storage.user"]}
        )

    await Tortoise.generate_schemas()  # move out into setup script to avoid multiprocessing problems
