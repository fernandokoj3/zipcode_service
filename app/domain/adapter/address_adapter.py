import app.use_case.viacep.viacep_retrieve_address as viacep_retrieve_address
from app.domain.port.zipcode_port import RetrieveAddressPort
from app.schema.response.zipcode_response import AddressResponse


class ViacepRetrieveAddressAdapter(RetrieveAddressPort):

    def __init__(self, zipcode: int | str):
        self._case = viacep_retrieve_address.ViacepRetrieveAddressAccount(
            zipcode=zipcode
        )
        super().__init__(zipcode)

    async def process(self) -> AddressResponse:
        return await self._case.execute()
