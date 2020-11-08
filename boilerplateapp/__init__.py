""" factoty method for FastAPI web service instance  """
from fastapi import FastAPI, Depends
from boilerplateapp.config import Configuration
from starlette_exporter import PrometheusMiddleware, handle_metrics
from boilerplateapp.storage import db_uri, metadata, database
import sqlalchemy

# setting configuration as a dependencies for easier reuse of the factory
def get_config():
    return Configuration()


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
        await database.connect()
   
    @app.on_event("shutdown")
    async def shutdown_db_connection():
        await database.disconnect()

    # midldeware prometheus
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)

    # routes
    from boilerplateapp.api.health import router
    app.include_router(
            router,
            prefix="",
            tags=[],
            dependencies=[Depends(get_config)],
            responses={}
            )

    from boilerplateapp.api.user import router as user_router
    app.include_router(
            user_router,
            prefix="",
            tags=[],
            dependencies=[],
            responses={}
            )

    return app
