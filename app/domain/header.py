import re
from typing import Optional

import jwt
from fastapi import Header
from fastapi.exceptions import RequestValidationError
from jwt import DecodeError
from pydantic import ValidationError

from app.schema.internal import HeaderRequest


def get_headers(
    authorization: Optional[str] = Header(
        None, alias="authorization", include_in_schema=True
    ),
) -> HeaderRequest:
    try:
        token = re.sub(
            r"Bearer\s?", "", authorization, flags=re.RegexFlag.IGNORECASE
        )
        payload = jwt.decode(token, options={"verify_signature": False})
        _client_id = payload.get("client_id")
        return HeaderRequest(client_id=_client_id)
    except ValidationError as e:
        raise RequestValidationError(
            [
                {
                    "loc": ("headers", "client_id"),
                    "msg": str(e.errors()[0].get("ctx").get("error")),
                    "type": "value_error",
                }
            ]
        )
    except DecodeError as e:
        raise RequestValidationError(
            [
                {
                    "loc": ("headers", "authorization"),
                    "msg": f"authorization required: '{authorization}' {str(e.args)}",
                    "type": "value_error",
                }
            ]
        )
