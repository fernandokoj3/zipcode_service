from fastapi import APIRouter, Depends, Path

from app.domain.factory.address_factory import create_find_address
from app.domain.port.zipcode_port import RetrieveAddressPort
from app.schema.response.zipcode_response import AddressResponse
from app.utils.settings import settings

router = APIRouter(prefix=f"{settings.base_url_v1}/zipcode", tags=["Zipcode"])


def _inject_find_address_by_zipcode(
    zipcode: str = Path(
        title="Zipcode value", pattern=r"^\d{5}-?\d{3}$", max_length=9
    )
) -> RetrieveAddressPort:
    return create_find_address(zipcode=zipcode)


@router.get(
    path="/{zipcode}",
    description="Route responsible retrieve address by zipcode",
    status_code=200,
    response_model=AddressResponse,
)
async def find_address_by_zipcode(
    case: RetrieveAddressPort = Depends(_inject_find_address_by_zipcode),
):
    return await case.process()
