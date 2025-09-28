from enum import Enum
from http import HTTPStatus
from typing import Any

import requests
from aiohttp import ClientResponseError, ClientSession
from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_exponential,
)


def should_retry(response: requests.Response) -> bool:
    return response.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR


def async_should_retry(response: Any) -> bool:
    return (
        isinstance(response, ClientResponseError)
        and response.status >= HTTPStatus.INTERNAL_SERVER_ERROR
    )


def return_last_value(retry_state: RetryCallState):
    """return the result of the last call attempt"""
    return retry_state.outcome.result()


class Method(Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    PATCH = "PATCH"


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry_error_callback=return_last_value,
    retry=retry_if_exception_type(
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError)
    )
    | retry_if_result(async_should_retry),
)
async def async_fetch_url(
    session: ClientSession, method: Method, url: str, **kwargs
):
    kwargs = {k: v for k, v in kwargs.items() if v}
    async with session.request(method.value, url=url, **kwargs) as res:
        res.raise_for_status()
        return await res.json()
