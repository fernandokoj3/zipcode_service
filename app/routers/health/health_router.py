from fastapi import APIRouter

from app.routers.health.schemas.ping_response import PingResponse
from app.utils.settings import settings

router = APIRouter()


@router.get(
    path="/",
    response_model=PingResponse,
    description="""Check health application""",
    include_in_schema=False,
)
async def ping():
    return {"pong": True, "version": settings.version}


@router.get(
    path="/version",
    description="Get",
    response_model=str,
    include_in_schema=False,
)
def get_version():
    """
    API version.
    """
    return settings.version
