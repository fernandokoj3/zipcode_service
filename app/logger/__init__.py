import contextvars
import logging
import sys
from typing import Any
from uuid import uuid4

import structlog
from structlog import get_logger
from structlog.contextvars import merge_contextvars
from structlog.processors import CallsiteParameter

logging.basicConfig(stream=sys.stdout, format="%(message)s")
correlation_context = contextvars.ContextVar("correlation_id", default=None)


def inject_correlation_id(_, __, event_dict):
    if correlation_id := correlation_context.get():
        event_dict["correlation_id"] = correlation_id
    else:
        correlation_id: Any = str(uuid4())
        correlation_context.set(correlation_id)
        event_dict["correlation_id"] = correlation_id
    return event_dict


def manual_inject(correlation_id: str = None):
    correlation_context.set(correlation_id or str(uuid4()))


structlog.configure(
    processors=[
        inject_correlation_id,
        merge_contextvars,
        structlog.threadlocal.merge_threadlocal,
        structlog.processors.CallsiteParameterAdder(
            [CallsiteParameter.FUNC_NAME, CallsiteParameter.MODULE]
        ),
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True, key="time-iso"),
        structlog.processors.JSONRenderer(sort_keys=True),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    # logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)


__all__ = [get_logger, manual_inject]
