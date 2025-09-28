from typing import Iterable

from fastapi import APIRouter, FastAPI
from fastapi.security import HTTPBearer

security = HTTPBearer()


def register_routes(app: FastAPI, routers: Iterable[APIRouter]):
    for router in routers:
        app.include_router(router)


def routes_config_v1(app: FastAPI):
    from app.routers.v1.address.address_router import router as address_router

    routers = (address_router,)
    register_routes(app, routers)


def routes_config_health(app: FastAPI) -> None:
    from app.routers.health.health_router import router as health_api

    register_routes(app, (health_api,))
