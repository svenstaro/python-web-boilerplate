""" factoty method for FastAPI web service instance  """
from fastapi import FastAPI, Depends
from application.config import Settings
from application.storage.db import db_uri, metadata
import sqlalchemy

# setting configuration as a dependencies for easier reuse of the factory
def get_config():
    return Settings()


# creating tables. each session/connection will be etsablished in separate APIRouter

def app_factory():
    """ Factory method for creating web service instacne and connecting to all middleware, routes, etc. """
    app = FastAPI(   
        title="Python Boilerplate",
        description="Basic python web service boilerplate with FastAPI",
        version="0.0.1"
        )

    # db initilalization
    @app.on_event("startup")
    async def start_dbs():
        engine = sqlalchemy.create_engine(db_uri)
        metadata.create_all(engine)
    
    # midldeware prometheus


    # middleware CORS


    # routes
    from application.api.health import router
    app.include_router(
            router,
            prefix="",
            tags=[],
            dependencies=[Depends(get_config)],
            responses={}
            )

    from application.api.user import router as usr_router
    app.include_router(
            usr_router,
            prefix="",
            tags=[],
            dependencies=[],
            responses={}
            )

    return app
