from abc import ABC, abstractmethod

from app.schema.response.zipcode_response import AddressResponse


class RetrieveAddressPort(ABC):

    def __init__(self, zipcode: str):
        self._zipcode = zipcode

    @abstractmethod
    async def process(self) -> AddressResponse:
        pass
