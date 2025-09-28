import aiohttp
from aiohttp import ClientResponseError, ClientSession

from app.domain.exceptions import (
    AppErrorCode,
    NotFoundException,
    UnprocessableEntity,
)
from app.logger import get_logger
from app.schema.response.zipcode_response import AddressResponse
from app.service.viacep_service import retrieve_address

log = get_logger(__name__)


class ViacepRetrieveAddressAccount:

    def __init__(self, zipcode: str):
        self._zipcode = zipcode

    async def execute(self) -> AddressResponse:
        log.info("Start retrieve address from zipcode", zipcode=self._zipcode)
        async with ClientSession(
            connector=aiohttp.TCPConnector(force_close=True)
        ) as session:
            try:
                viacep_response = await retrieve_address(
                    zipcode=self._zipcode, session=session
                )
                return AddressResponse(**viacep_response.model_dump())

            except NotFoundException as e:
                log.error("Zipcode not found", zipcode=self._zipcode)
                raise e

            except ClientResponseError as e:
                log.error(
                    "Fail to retrieve zipcode",
                    zipcode=self._zipcode,
                    error=e.message,
                )
                raise UnprocessableEntity(
                    app_error_code=AppErrorCode.ERROR_UNPROCESSABLE,
                    msg=f"Fail to retrieve address from zipcode {self._zipcode}",
                )
