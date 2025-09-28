from aiohttp import ClientSession

from app.domain.exceptions import AppErrorCode, NotFoundException
from app.schema.internal.viacep.response.viacep_response import (
    ERROR_TAG,
    ViaCepResponse,
)
from app.service.service_api import Method, async_fetch_url
from app.utils.settings import DEFAULT_VIACEP_BASE_URL


async def retrieve_address(
    session: ClientSession, *, zipcode: str
) -> ViaCepResponse:
    url = "{base_url}/ws/{zipcode}/json/".format(
        base_url=DEFAULT_VIACEP_BASE_URL, zipcode=zipcode
    )

    response = await async_fetch_url(
        session=session, method=Method.GET, url=url
    )
    if ERROR_TAG in response:
        raise NotFoundException(
            app_error_code=AppErrorCode.ERROR_NOT_FOUND,
            msg=f"Zipcode {zipcode} not found",
        )
    return ViaCepResponse(**response)
