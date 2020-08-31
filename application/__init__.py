""" factoty method for FastAPI web service instance  """
from fastapi import FastAPI, Depends
from application.config import Settings
from application.storage import db_init
from tortoise import run_async

# setting configuration as a dependencies for easier reuse of the factory
def get_config():
    return Settings()


def app_factory():
    """ Factory method for creating web service instacne and connecting to all middleware, routes, etc. """
    app = FastAPI(   
        title="Python Boilerplate",
        description="Basic python web service boilerplate with FastAPI",
        version="0.0.1"
        )
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
    
    # db connection init
    run_async(db_init())

    return app
