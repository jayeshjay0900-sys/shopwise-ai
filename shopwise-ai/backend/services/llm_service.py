from __future__ import annotations

import asyncio
import json
import logging
from typing import Any
import httpx
from backend.config import settings


class LLMServiceError(RuntimeError):
    pass


class LLMService:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key if api_key is not None else settings.groq_api_key

    async def structured(self, system: str, user: str, schema: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            logging.getLogger("shopwise.llm").error("Groq key unavailable in runtime")
            raise LLMServiceError("missing GROQ_API_KEY")
        payload = {"model": settings.groq_model, "temperature": 0.1, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "response_format": {"type": "json_object"}}
        for attempt in range(2):
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    response = await client.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}"}, json=payload)
                    response.raise_for_status()
                    content = response.json()["choices"][0]["message"]["content"]
                    parsed = json.loads(content)
                    if not isinstance(parsed, dict):
                        raise ValueError("structured response was not an object")
                    return parsed
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                logging.getLogger("shopwise.llm").warning("Groq network failure: %s", type(exc).__name__)
                if attempt == 0:
                    await asyncio.sleep(0.15)
                    continue
                raise LLMServiceError("Groq structured response failed") from exc
            except (httpx.HTTPError, KeyError, ValueError, json.JSONDecodeError) as exc:
                status = exc.response.status_code if isinstance(exc, httpx.HTTPStatusError) else "n/a"
                code = "unknown"
                if isinstance(exc, httpx.HTTPStatusError):
                    try:
                        error_payload = exc.response.json().get("error", {})
                        code = error_payload.get("code") or error_payload.get("type") or "unknown"
                    except (ValueError, TypeError, AttributeError):
                        pass
                logging.getLogger("shopwise.llm").warning("Groq response failure: kind=%s status=%s code=%s", type(exc).__name__, status, code)
                raise LLMServiceError("Groq structured response failed") from exc
        raise LLMServiceError("Groq structured response failed")
