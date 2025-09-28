from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from typing import Optional, Union

from werkzeug.exceptions import HTTPException


@dataclass
class InfoAppErrorCode(object):
    code: int = 0
    description: Optional[str] = None


class AppErrorCode(Enum):
    """Application code errors"""

    ERROR_GENERIC = InfoAppErrorCode(1, "Generic error.")
    ERROR_UNAUTHORIZED = InfoAppErrorCode(2, "Not authorized.")
    ERROR_FORBIDDEN = InfoAppErrorCode(3, "Forbidden access.")
    ERROR_NOT_FOUND = InfoAppErrorCode(4, "Not found.")
    ERROR_BAD_REQUEST = InfoAppErrorCode(5, "Bad request.")
    ERROR_UNPROCESSABLE = InfoAppErrorCode(4, "Request error related.")
    UNAVAILABLE_SERVICE = InfoAppErrorCode(7, "Service unavailable.")


class ApplicationException(HTTPException):
    def __init__(
        self,
        app_error_code: AppErrorCode,
        msg: str = None,
        detail: any = None,
        http_error_code: int = None,
    ):
        err_code, err_msg = self._read_error_code_msg(app_error_code, msg)
        self.app_error_code = err_code
        self.description = err_msg
        self.detail = detail
        self.code = (
            http_error_code
            if http_error_code
            else HTTPStatus.INTERNAL_SERVER_ERROR
        )

    @staticmethod
    def _read_error_code_msg(app_error_code, msg):
        err_code = app_error_code
        err_msg = msg
        if isinstance(app_error_code, AppErrorCode):
            app_error_code = app_error_code.value
            err_code = app_error_code.code
            if err_msg is None:
                err_msg = app_error_code.description
        if err_msg is None:
            err_msg = "Erro interno no servidor"
        return err_code, err_msg


class NotFoundException(ApplicationException):
    def __init__(
        self,
        app_error_code,
        msg: str = None,
        detail: any = None,
    ):
        super(NotFoundException, self).__init__(
            app_error_code, msg, detail, HTTPStatus.NOT_FOUND
        )


class BadRequestException(ApplicationException):
    def __init__(
        self,
        app_error_code,
        msg: Union[str, list] = None,
        detail: any = None,
    ):
        super(BadRequestException, self).__init__(
            app_error_code, msg, detail, HTTPStatus.BAD_REQUEST
        )


class UnprocessableEntity(ApplicationException):
    def __init__(
        self,
        app_error_code,
        msg: Union[str, list] = None,
        detail: any = None,
    ):
        super(UnprocessableEntity, self).__init__(
            app_error_code, msg, detail, HTTPStatus.UNPROCESSABLE_ENTITY
        )


class ForbiddenException(ApplicationException):
    def __init__(
        self,
        msg: Union[str, list] = None,
        detail: any = None,
    ):
        super(ForbiddenException, self).__init__(
            AppErrorCode.ERROR_FORBIDDEN, msg, detail, HTTPStatus.FORBIDDEN
        )


class NotAuthorizerException(ApplicationException):
    def __init__(
        self,
        msg: Union[str, list] = None,
        detail: any = None,
    ):
        super(NotAuthorizerException, self).__init__(
            AppErrorCode.ERROR_UNAUTHORIZED,
            msg,
            detail,
            HTTPStatus.UNAUTHORIZED,
        )
