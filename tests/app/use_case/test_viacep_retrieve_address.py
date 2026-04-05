from re import sub

import pytest
from aioresponses import aioresponses
from faker import Faker

from app.domain.exceptions import NotFoundException, UnprocessableEntity
from app.use_case.viacep.viacep_retrieve_address import (
    ViacepRetrieveAddressAccount as Subject,
)
from app.utils.settings import settings

my_faker = Faker("pt_BR")


@pytest.fixture()
def create_response(request):
    param = request.param if hasattr(request, "param") else dict()
    local_postcode = param.get("postcode", my_faker.postcode())
    postcode = sub(r"(\d{5})(\d{3})", r"\1-\2", local_postcode)

    return {
        "cep": postcode,
        "logradouro": param.get("logradouro", my_faker.street_name()),
        "complemento": param.get("complemento", my_faker.street_suffix()),
        "bairro": param.get(
            "bairro", my_faker.bairro()
        ),  # bairro existe no provider pt_BR
        "localidade": param.get("localidade", my_faker.city()),
        "unidade": param.get("unidade", ""),
        "uf": param.get("uf", my_faker.estado_sigla()),
        "estado": param.get("estado", my_faker.estado_nome()),
        "regiao": param.get("regiao", "Sudeste"),
        "ibge": param.get(
            "ibge", my_faker.random_number(digits=7, fix_len=True)
        ),
        "gia": param.get("gia", str(my_faker.random_int(min=1000, max=9999))),
        "ddd": param.get("ddd", str(my_faker.random_int(min=11, max=99))),
        "siafi": param.get(
            "siafi", str(my_faker.random_int(min=1000, max=9999))
        ),
    }


@pytest.fixture()
def aiohttp_mock():
    with aioresponses() as m:
        yield m


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_response",
    [dict(postcode="01001-000")],
    indirect=True,
)
async def test_given_valid_zipcode_viacep_retrieve_address_should_return_ok(
    create_response, aiohttp_mock
):
    url = "{base_url}/ws/{zipcode}/json/".format(
        base_url=settings.viacep_base_url, zipcode="01001-000"
    )

    aiohttp_mock.get(url=url, status=200, payload=create_response)

    result = await Subject(zipcode="01001-000").execute()
    assert result
    assert result.zipcode
    assert result.street
    assert result.complement
    assert result.neighborhood
    assert result.city
    assert result.state_code
    assert result.state
    assert result.region
    assert not result.unit


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_response",
    [dict(postcode="01472-900")],
    indirect=True,
)
async def test_given_valid_zipcode_viacep_retrieve_address_should_return_with_same_zipcode(
    create_response,
    aiohttp_mock,
):
    url = "{base_url}/ws/{zipcode}/json/".format(
        base_url=settings.viacep_base_url, zipcode="01472-900"
    )

    aiohttp_mock.get(url=url, status=200, payload=create_response)

    result = await Subject(zipcode="01472-900").execute()
    assert result
    assert result.zipcode
    assert result.zipcode == "01472900"


@pytest.mark.asyncio
async def test_given_invalid_zipcode_viacep_retrieve_address_should_return_not_found(
    aiohttp_mock,
):
    url = "{base_url}/ws/{zipcode}/json/".format(
        base_url=settings.viacep_base_url, zipcode="01001-999"
    )

    aiohttp_mock.get(url=url, status=200, payload={"erro": True})

    with pytest.raises(NotFoundException) as exc_info:
        await Subject(zipcode="01001-999").execute()

    assert exc_info.value.description == "Zipcode 01001-999 not found"


@pytest.mark.asyncio
async def test_given_invalid_zipcode_viacep_retrieve_address_should_return_error(
    aiohttp_mock,
):
    url = "{base_url}/ws/{zipcode}/json/".format(
        base_url=settings.viacep_base_url, zipcode="01001-999"
    )

    aiohttp_mock.get(url=url, status=500, payload=None)

    with pytest.raises(UnprocessableEntity) as exc_info:
        await Subject(zipcode="01001-999").execute()

    assert (
        exc_info.value.description
        == "Fail to retrieve address from zipcode 01001-999"
    )
