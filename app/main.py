from fastapi import FastAPI
from mangum import Mangum

from app import bootstrap
from app.middleware.correlation_middleware import CorrelationMiddleware

TAGS_METADATA = [
    {
        "name": "Address",
        "description": "Responsible to get address from zipcode",
    },
]


async def _fastapi_startup(fastapi: FastAPI):
    from app.config.error_handler import configure_exception_handlers
    from app.routers import routes_config_health, routes_config_v1

    await bootstrap.startup()

    routes_config_health(fastapi)
    routes_config_v1(fastapi)

    configure_exception_handlers(fastapi)


async def _fastapi_shutdown(_: FastAPI):
    await bootstrap.shutdown()


# noinspection PyTypeChecker
def create_fastapi_application() -> FastAPI:
    from fastapi import FastAPI

    from app.utils.settings import settings

    async def _startup():
        await _fastapi_startup(fastapi)

    async def _shutdown():
        await _fastapi_shutdown(fastapi)

    fastapi = FastAPI(
        title="Zicode Service",
        version=settings.version,
        on_startup=[_startup],
        on_shutdown=[_shutdown],
        openapi_tags=TAGS_METADATA,
        docs_url=f"{settings.base_url_v1}/zipcode/docs",
        redoc_url=f"{settings.base_url_v1}/zipcode/redocs",
        openapi_url=f"{settings.base_url_v1}/zipcode/openapi.json",
    )

    from app.config.error_handler import configure_exception_handlers

    configure_exception_handlers(fastapi)
    fastapi.add_middleware(CorrelationMiddleware)

    return fastapi


app = create_fastapi_application()
handler = Mangum(app)

"""
For LOCAL development
"""
if __name__ == "__main__":
    # Start singles
    import uvicorn

    uvicorn.run(
        "app.main:create_fastapi_application",
        host="0.0.0.0",  # nosec
        port=5000,
        reload=True,
        log_level="info",
    )
