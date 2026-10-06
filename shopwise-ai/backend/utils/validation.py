from __future__ import annotations

from urllib.parse import urlparse
from typing import Any


def is_safe_http_url(value: str | None) -> bool:
    if not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def clean_url(value: Any) -> str | None:
    if isinstance(value, str) and is_safe_http_url(value.strip()):
        return value.strip()
    return None


def valid_search_result(item: dict[str, Any]) -> bool:
    return bool(clean_url(item.get("url")) and str(item.get("title", "")).strip())


def verified_url_list(values: list[Any]) -> list[str]:
    return [url for value in values if (url := clean_url(value))]
