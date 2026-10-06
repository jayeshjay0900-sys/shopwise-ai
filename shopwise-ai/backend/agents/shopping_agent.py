from __future__ import annotations
import logging

from backend.agents.product_researcher import product_evidence, research_products, review_evidence
from backend.agents.recommender import build_awards, build_comparison, make_recommendation, rank_products
from backend.agents.requirement_parser import parse_requirements
from backend.agents.review_analyzer import analyze_reviews
from backend.models.product import Product
from backend.models.recommendation import ChatResponse
from backend.models.search import ChatRequest, Requirements
from backend.services.llm_service import LLMService, LLMServiceError
from backend.services.product_service import evidence_to_products, merge_analysis, validate_products
from backend.services.tavily_service import TavilyService, TavilyServiceError

logger = logging.getLogger("shopwise.agent")


class ShoppingAgent:
    def __init__(self, tavily: TavilyService | None = None, llm: LLMService | None = None) -> None:
        self.tavily = tavily or TavilyService()
        self.llm = llm or LLMService()

    async def run(self, request: ChatRequest, previous: Requirements | None = None, previous_products: list[Product] | None = None) -> ChatResponse:
        structured: dict = {}
        try:
            structured = await self.llm.structured(
                "Extract shopping requirements as JSON only. Keys: category, brand, product_family, budget_max, currency, use_case, required_features, excluded_products. Use null for unspecified fields. Never infer or invent a budget; preserve the user's explicit category, brand, family, and features.",
                request.message,
                {},
            )
        except (LLMServiceError, ValueError, TypeError) as exc:
            logger.warning("Query understanding unavailable; using deterministic parser: %s", type(exc).__name__)
        requirements = parse_requirements(request.message, previous, structured)
        lower = request.message.lower()
        category_changed = bool(previous and requirements.product_type != "not available" and requirements.product_type != previous.product_type)
        new_search_intent = any(token in lower for token in ("find", "search", "show", "under ₹", "under rs", "under inr", "best laptop", "best phone", "best headphones", "now"))
        follow_up = bool(previous_products) and not category_changed and not new_search_intent
        if follow_up:
            compatible = [product for product in previous_products or [] if product.product_type == requirements.product_type]
            ranked = rank_products(compatible, requirements)
            return ChatResponse(assistant_message="Using the compatible options already researched, here is the answer against your follow-up.", requirements=requirements, products=ranked, recommendation=make_recommendation(ranked, requirements), comparison=build_comparison(ranked[:3]), awards=build_awards(ranked), evidence_count=sum(len(p.evidence) for p in ranked))
        try:
            results = await research_products(self.tavily, requirements)
        except TavilyServiceError as exc:
            logger.warning("Web research failure: %s", str(exc))
            raise RuntimeError("Web research is temporarily unavailable.") from exc
        products = validate_products(evidence_to_products(product_evidence(results), requirements), requirements)
        if not products:
            return ChatResponse(assistant_message=f"No reliable products were found: no verified {requirements.category.lower()} product pages matched your requirements.", requirements=requirements)
        reviews = review_evidence(results)
        ai_limited = False
        try:
            for product in products[:4]:
                labelled_product = "\n".join(f"[{item.source_type}] {item.url}\n{item.snippet[:1200]}" for item in product.evidence)
                try:
                    analysis = await self.llm.structured("Return exactly one JSON object with keys price (number or null), rating (number or null), review_count (integer or null), specifications (object of string keys and values), pros (array of strings), cons (array of strings), and review_summary (string). Extract only verifiable product facts from labelled evidence; do not add markdown or wrapper keys.", f"Product: {product.name}\nEvidence:\n{labelled_product}", {})
                    merge_analysis(product, analysis)
                except (LLMServiceError, ValueError, TypeError) as exc:
                    logger.warning("AI product enrichment limited: %s", type(exc).__name__)
                    ai_limited = True
                    break
            if not ai_limited:
                for product in products[:4]:
                    product_tokens = [token.lower() for token in product.name.split() if len(token) >= 4]
                    matching_reviews = [item for item in reviews if any(token in f"{item.title} {item.content}".lower() for token in product_tokens)]
                    review_text = "\n".join(f"[review source] {item.url}\n{item.content[:1200]}" for item in matching_reviews[:3])
                    if not review_text:
                        continue
                    try:
                        await analyze_reviews(product, review_text, [str(item.url) for item in matching_reviews[:3]], self.llm)
                    except (LLMServiceError, ValueError, TypeError) as exc:
                        logger.warning("AI review enrichment limited: %s", type(exc).__name__)
                        ai_limited = True
                        break
        except (ValueError, TypeError) as exc:
            logger.warning("AI analysis normalization failure: %s", type(exc).__name__)
            ai_limited = True
        ranked = rank_products(validate_products(products, requirements), requirements)
        recommendation = make_recommendation(ranked, requirements)
        message = f"Searching for: \"{requirements.raw_query}\"."
        if recommendation:
            message += f" Strongest match: {recommendation.product.name}. {recommendation.why}"
        else:
            message += f" I found only {len(ranked)} strong matches for your requirements."
        if ai_limited:
            message += " AI enrichment is temporarily rate-limited, so unavailable fields are clearly marked rather than guessed."
        return ChatResponse(assistant_message=message, requirements=requirements, products=ranked, recommendation=recommendation, comparison=build_comparison(ranked[:3]), awards=build_awards(ranked), evidence_count=sum(len(p.evidence) for p in ranked))
