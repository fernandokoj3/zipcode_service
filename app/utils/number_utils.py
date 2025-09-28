from re import sub
from typing import Any, Final

DEFAULT_PATTERN_EXTRACT_NUMBER: Final[str] = r"[^0-9]"


def only_numbers(value: str) -> Any:
    return sub(DEFAULT_PATTERN_EXTRACT_NUMBER, "", value)
