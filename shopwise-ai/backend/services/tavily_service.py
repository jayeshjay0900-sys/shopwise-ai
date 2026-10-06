from __future__ import annotations

import asyncio
import logging
from typing import Any
from urllib.parse import urlparse
import httpx
from backend.config import settings
from backend.models.product import ResearchResult
from backend.models.search import Requirements, SearchQuery
from backend.utils.validation import valid_search_result


class TavilyServiceError(RuntimeError):
    pass


def _safe_image_url(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlparse(value)
    return value if parsed.scheme in {"http", "https"} and parsed.netloc else None


class TavilyService:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key if api_key is not None else settings.tavily_api_key

    def build_queries(self, requirements: Requirements) -> list[SearchQuery]:
        category = requirements.category
        budget = f"under ₹{requirements.budget:,.0f}" if requirements.budget else ""
        identity = " ".join(item for item in (requirements.brand, requirements.model_family) if item != "Not available")
        constraints = " ".join([identity, *requirements.must_have, *requirements.use_cases, *requirements.preferences]).strip()
        queries = [SearchQuery(query=f"{identity or category} {category} actual products {budget} India official specifications {constraints}".strip(), purpose="product discovery"), SearchQuery(query=f"{identity or category} exact model names {budget} India retailer price".strip(), purpose="price verification"), SearchQuery(query=f"{identity or category} exact model reviews {constraints} India".strip(), purpose="review research")]
        if category == "Laptop":
            queries.extend([SearchQuery(query=f"gaming laptops RTX {budget} India actual models", purpose="product discovery"), SearchQuery(query=f"RTX 4060 laptop {budget} India product", purpose="product discovery"), SearchQuery(query=f"RTX 4050 laptop {budget} India product", purpose="product discovery")])
        elif category == "Phone":
            queries.append(SearchQuery(query=f"smartphone actual models {budget} India camera battery product", purpose="product discovery"))
        return queries

    async def search(self, query: str, max_results: int = 6) -> list[ResearchResult]:
        if not self.api_key:
            logging.getLogger("shopwise.tavily").error("Tavily key unavailable in runtime")
            raise TavilyServiceError("missing TAVILY_API_KEY")
        payload = {"api_key": self.api_key, "query": query, "search_depth": "advanced", "max_results": max_results, "include_answer": False, "include_images": True}
        for attempt in range(2):
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    response = await client.post("https://api.tavily.com/search", json=payload)
                    response.raise_for_status()
                    items: list[dict[str, Any]] = response.json().get("results", [])
                    return [ResearchResult(title=item["title"], url=item["url"], content=item.get("content", ""), score=item.get("score"), image_url=_safe_image_url(item.get("image_url") or item.get("image"))) for item in items if valid_search_result(item)]
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                logging.getLogger("shopwise.tavily").warning("Tavily network failure: %s", type(exc).__name__)
                if attempt == 0:
                    await asyncio.sleep(0.15)
                    continue
                raise TavilyServiceError("Tavily search failed") from exc
            except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
                logging.getLogger("shopwise.tavily").warning("Tavily response failure: %s", type(exc).__name__)
                raise TavilyServiceError("Tavily search failed") from exc
        raise TavilyServiceError("Tavily search failed")
