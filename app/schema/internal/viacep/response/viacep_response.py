from typing import Final, Optional

from pydantic import BaseModel, Field

ERROR_TAG: Final[str] = "erro"


class ViaCepResponse(BaseModel):
    zipcode: Optional[str] = Field(None, alias="cep")
    street: Optional[str] = Field(None, alias="logradouro")
    complement: Optional[str] = Field(None, alias="complemento")
    unit: Optional[str] = Field(None, alias="unidade")
    neighborhood: Optional[str] = Field(None, alias="bairro")
    city: Optional[str] = Field(None, alias="localidade")
    state_code: Optional[str] = Field(None, alias="uf")
    state: Optional[str] = Field(None, alias="estado")
    region: Optional[str] = Field(None, alias="regiao")
