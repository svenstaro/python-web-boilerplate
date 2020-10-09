""" factoty method for FastAPI web service instance  """
from fastapi import FastAPI, Depends
from application.config import Settings
from starlette_exporter import PrometheusMiddleware, handle_metrics
from application.storage import db_uri, metadata, User, UserTokens
import sqlalchemy

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

    # db initilalization
    @app.on_event("startup")
    async def start_dbs():
        engine = sqlalchemy.create_engine(db_uri)
        metadata.create_all(engine)
        await User.__database__.connect()
        await UserTokens.__database__.connect()
   
    @app.on_event("shutdown")
    async def shutdown_db_connection():
        await User.__database__.close()
        await UserTokens.__database__.close()

    # midldeware prometheus
    app.add_middleware(PrometheusMiddleware, app_name="boilerplate", prefix='fastapi_boilerplate')
    app.add_route("/metrics", handle_metrics)

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
