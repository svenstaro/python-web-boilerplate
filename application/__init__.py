""" factoty method for FastAPI web service instance  """
from fastapi import FastAPI


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
            dependencies=[],
            responses={}
            )


    return app
