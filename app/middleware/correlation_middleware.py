import contextvars
from uuid import uuid4

import structlog.contextvars
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class CorrelationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        correlation_id = contextvars.ContextVar(
            "correlation_id",
            default=request.headers.get("X-Correlation-ID", str(uuid4())),
        )
        structlog.contextvars.bind_contextvars(
            correlation_id=correlation_id.get()
        )
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id.get()
        return response
