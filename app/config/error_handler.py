from http import HTTPStatus
from typing import TYPE_CHECKING

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.domain.exceptions import ApplicationException
from app.logger import get_logger

if TYPE_CHECKING:
    from fastapi import FastAPI, Request, Response

log = get_logger(__name__)


async def _handle_application_exception(
    _: "Request", exc: ApplicationException
) -> "Response":
    err = {
        "detail": exc.detail,
        "code": exc.app_error_code,
        "message": exc.description,
    }
    response = JSONResponse(
        status_code=exc.code,
        content=jsonable_encoder({k: v for k, v in err.items() if v}),
    )

    log.info("RESPONSE ERROR", response=response)
    return response


async def _handle_request_validation_exception(
    _: "Request", exc: RequestValidationError
) -> "Response":
    for error in exc.errors():
        error["message"] = error.pop("msg")

    response = JSONResponse(
        content=jsonable_encoder({"detail": exc.errors()}),
        status_code=HTTPStatus.BAD_REQUEST,
    )
    log.info("VALIDATION ERROR", response=exc.errors())
    return response


async def _handle_validation_exception(
    _: "Request", exc: ValidationError
) -> "Response":
    res = []
    for error in exc.errors():
        res.append(
            dict(msg=error["msg"], loc=error["loc"], type=error["type"])
        )

    response = JSONResponse(
        content=jsonable_encoder({"detail": res}),
        status_code=HTTPStatus.BAD_REQUEST,
    )
    log.info("VALIDATION ERROR", response=exc.errors())
    return response


def configure_exception_handlers(app: "FastAPI") -> None:
    handlers = (
        (ApplicationException, _handle_application_exception),
        (RequestValidationError, _handle_request_validation_exception),
        (ValidationError, _handle_validation_exception),
    )

    for exception, handler in handlers:
        app.add_exception_handler(exception, handler)
