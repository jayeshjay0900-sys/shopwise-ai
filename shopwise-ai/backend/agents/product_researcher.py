from __future__ import annotations

from backend.models.product import ResearchResult
from backend.models.search import Requirements
from backend.services.tavily_service import TavilyService


async def research_products(tavily: TavilyService, requirements: Requirements) -> list[ResearchResult]:
    results: list[ResearchResult] = []
    for query in tavily.build_queries(requirements):
        query_text = query["query"] if isinstance(query, dict) else query.query
        purpose = query.get("purpose", "web") if isinstance(query, dict) else query.purpose
        for result in await tavily.search(query_text):
            results.append(result.model_copy(update={"purpose": purpose}) if hasattr(result, "model_copy") else result)
    return results


def product_evidence(results: list[ResearchResult]) -> list[ResearchResult]:
    return [result for result in results if result.purpose in {"product discovery", "price verification"}]


def review_evidence(results: list[ResearchResult]) -> list[ResearchResult]:
    return [result for result in results if result.purpose == "review research"]
