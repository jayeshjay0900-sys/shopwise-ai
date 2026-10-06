from __future__ import annotations
from backend.models.product import Product
import re
from backend.models.search import Requirements


def _matches(requirement: str, searchable: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", " ", searchable.lower())
    alternatives = [part.strip() for part in requirement.lower().split("/") if part.strip()]
    return any(all(token in normalized.split() for token in re.sub(r"[^a-z0-9]+", " ", alt).split()) for alt in alternatives)


def score_product(product: Product, requirements: Requirements) -> tuple[int, str]:
    if requirements.budget is not None:
        budget_fit = 0.7 if product.price is None else max(0.0, min(1.0, 1 - max(product.price - requirements.budget, 0) / requirements.budget))
        budget_label = "within budget" if product.price is not None and product.price <= requirements.budget else ("budget is unverified" if product.price is None else "above target budget")
    else:
        budget_fit, budget_label = 0.7, "budget was not specified"
    searchable = " ".join([product.name, product.brand, *product.specifications.keys(), *product.specifications.values(), *product.pros]).lower()
    requested_identity = [item for item in (requirements.brand, requirements.model_family) if item != "Not available"]
    identity_matches = sum(1 for item in requested_identity if item.lower() in searchable)
    identity_fit = identity_matches / len(requested_identity) if requested_identity else 0.7
    requested = list(dict.fromkeys(requirements.must_have + requirements.preferences))
    matches = [item for item in requested if _matches(item, searchable)]
    feature_fit = (len(matches) + 0.5 * (len(requested) - len(matches))) / max(1, len(requested))
    use_case_matches = [item for item in requirements.use_cases if _matches(item, searchable)]
    use_case_fit = (len(use_case_matches) + 0.5 * (len(requirements.use_cases) - len(use_case_matches))) / max(1, len(requirements.use_cases)) if requirements.use_cases else 0.7
    quality_fit = (product.rating or 0) / 5 if product.rating is not None else 0.55
    review_fit = (product.sentiment.positive / 100) if product.sentiment else 0.55
    score = round((budget_fit * .25 + identity_fit * .15 + feature_fit * .25 + use_case_fit * .15 + quality_fit * .1 + review_fit * .1) * 100)
    labels = [f"Budget match: {budget_label}", f"Brand/model: {identity_matches}/{max(1, len(requested_identity))}", f"Requirements: {len(matches)}/{max(1, len(requested))}", f"Use cases: {len(use_case_matches)}/{max(1, len(requirements.use_cases))}", "Review/value signals: available" if product.sentiment or product.rating else "Review/value signals: unavailable"]
    return max(0, min(100, score)), "; ".join(labels) + "."
