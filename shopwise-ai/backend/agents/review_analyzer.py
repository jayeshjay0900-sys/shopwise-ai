from __future__ import annotations

import logging
import re
from typing import Any
from pydantic import ValidationError
from backend.models.product import Product, ReviewAnalysis
from backend.services.llm_service import LLMService

logger = logging.getLogger("shopwise.reviews")


def _number(value: Any, default: int) -> int:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return max(0, min(100, int(value)))
    match = re.search(r"\d+", str(value or ""))
    return max(0, min(100, int(match.group(0)))) if match else default


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [part.strip(" •-\t") for part in re.split(r"\n|;", value) if part.strip()][:5]
    if isinstance(value, list):
        return [str(item.get("text", item.get("name", item))) if isinstance(item, dict) else str(item) for item in value][:5]
    return []


def _unwrap(data: dict[str, Any]) -> dict[str, Any]:
    for key in ("review_analysis", "reviews", "result", "data"):
        value = data.get(key)
        if isinstance(value, dict):
            return value
    return data


async def analyze_reviews(product: Product, review_evidence: str, review_urls: list[str], llm: LLMService) -> Product:
    system = "Return exactly one JSON object with keys pros (array of strings), cons (array of strings), summary (string), sentiment (object with integer positive, neutral, negative percentages totaling 100), and review_urls (array). Select review_urls only from the supplied evidence URLs. Never invent facts."
    user = f"Product: {product.name}\nAllowed review URLs: {review_urls}\nReview evidence:\n{review_evidence[:7000]}"
    data = await llm.structured(system, user, {})
    raw = _unwrap(data)
    raw_sentiment = raw.get("sentiment")
    sentiment: dict[str, Any] = raw_sentiment if isinstance(raw_sentiment, dict) else {}
    if not all(key in sentiment for key in ("positive", "neutral", "negative")):
        logger.info("Review evidence returned without complete sentiment; leaving sentiment unavailable")
        return product
    positive, neutral, negative = _number(sentiment.get("positive"), 0), _number(sentiment.get("neutral"), 0), _number(sentiment.get("negative"), 0)
    total = max(1, positive + neutral + negative)
    normalized = {"pros": _strings(raw.get("pros")), "cons": _strings(raw.get("cons")), "summary": str(raw.get("summary") or raw.get("review_summary") or "Not available"), "sentiment": {"positive": round(positive * 100 / total), "neutral": round(neutral * 100 / total), "negative": round(negative * 100 / total)}, "review_urls": [str(url) for url in raw.get("review_urls", [])] if isinstance(raw.get("review_urls"), list) else []}
    try:
        analysis = ReviewAnalysis.model_validate(normalized)
    except ValidationError as exc:
        logger.warning("Review analysis validation fallback: %s", len(exc.errors()))
        return product
    allowed = set(review_urls)
    product.pros = analysis.pros
    product.cons = analysis.cons
    product.review_summary = analysis.summary
    product.sentiment = analysis.sentiment
    product.review_urls = [url for url in analysis.review_urls if url in allowed]
    product.source_urls = list(dict.fromkeys([*product.source_urls, *product.review_urls]))
    return product
