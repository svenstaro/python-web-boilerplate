""" factoty method for FastAPI web service instance  """
from fastapi import FastAPI, Depends
from application.config import Settings
from application.storage import db_init
from tortoise import Tortoise


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

    from application.api.user import router as usr_router
    app.include_router(
            usr_router,
            prefix="",
            tags=[],
            dependencies=[],
            responses={}
            )
    
    # db connection init
    @app.on_event("startup")
    async def startup_event():
        await db_init()

    @app.on_event("shutdown")
    async def shutdown_event():
        await Tortoise.close_connections()

    return app
