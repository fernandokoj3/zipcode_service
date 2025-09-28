from app.domain.adapter.address_adapter import (
    ViacepRetrieveAddressAdapter,
)
from app.logger import get_logger

log = get_logger(__name__)


def create_find_address(
    zipcode: str, name: str = "viacep"
) -> ViacepRetrieveAddressAdapter:
    match name.lower():
        case "viacep":
            log.info("Start retrieve address using viacep")
            return ViacepRetrieveAddressAdapter(zipcode=zipcode)
        case _:
            log.info("[FALLBACK] Start retrieve address using viacep")
            return ViacepRetrieveAddressAdapter(zipcode=zipcode)
