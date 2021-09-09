from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware import authentication, cors

from janusbackup.api.middleware import JWTAuthBackend
from janusbackup.api.routes import api_router
from janusbackup.api.utils.exception_handler import exception_handlers

# from janusbackup.database.instance import init_db

__all__ = ["get_app"]


def get_app(config) -> FastAPI:
    # docs_config = (
    #     {
    #         "docs_url": "/api/docs/",
    #         "redoc_url": "/api/redocs/",
    #         "openapi_url": "/api/docs/openapi.json",
    #     }
    #     if not IS_PRODUCTION
    #     else {}
    # )

    app = FastAPI(
        title="JanusBackup",
        exception_handlers=exception_handlers,
        # **docs_config,
    )

    # init_db(app)

    #########
    # Routes
    ##########

    app.include_router(api_router, prefix="/api")

    ##########
    # Middlewares
    ##########

    app.add_middleware(
        cors.CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(authentication.AuthenticationMiddleware, backend=JWTAuthBackend())

    ##########
    # Misc
    ##########

    SentryAsgiMiddleware(app)

    return app
