from __future__ import annotations
from backend.models.product import Product
from backend.models.recommendation import ComparisonRow, Recommendation
from backend.models.search import Requirements
from backend.utils.scoring import score_product


def rank_products(products: list[Product], requirements: Requirements) -> list[Product]:
    for product in products:
        product.match_score, product.score_explanation = score_product(product, requirements)
    return sorted(products, key=lambda item: item.match_score, reverse=True)


def build_awards(products: list[Product]) -> dict[str, str]:
    if not products: return {}
    value_pool = [p for p in products if p.price is not None]
    performance = max(products, key=lambda p: ((p.rating or 0), len(p.specifications)))
    value = min(value_pool, key=lambda p: p.price if p.price is not None else float("inf")) if value_pool else products[0]
    return {"Best Overall": products[0].name, "Best Value": value.name, "Best Performance": performance.name, "Best for Your Use Case": products[0].name}


def build_comparison(products: list[Product]) -> list[ComparisonRow]:
    rows: list[ComparisonRow] = []
    for feature, getter in [("Price", lambda p: f"{p.currency} {p.price:,.0f}" if p.price is not None else "Price not verified"), ("Rating", lambda p: f"{p.rating:.1f}/5" if p.rating is not None else "Not available"), ("AI Match", lambda p: f"{p.match_score}%"), ("Key specs", lambda p: ", ".join(f"{k}: {v}" for k, v in list(p.specifications.items())[:2]) or "Not available")]:
        rows.append(ComparisonRow(feature=feature, values={p.name: getter(p) for p in products}))
    return rows


def make_recommendation(products: list[Product], requirements: Requirements) -> Recommendation | None:
    if not products: return None
    product = products[0]
    reasons: list[str] = []
    if requirements.brand != "Not available": reasons.append(f"matches the requested {requirements.brand} brand")
    if requirements.model_family != "Not available": reasons.append(f"matches the {requirements.model_family} family")
    if product.price is not None and requirements.budget is not None and product.price <= requirements.budget: reasons.append("has a verified price within budget")
    if product.specifications: reasons.append("has the strongest verified specifications among the filtered options")
    if product.sentiment: reasons.append("has retrieved review sentiment")
    why = f"{product.name} is the strongest match because " + ", ".join(reasons or ["it has the highest evidence-backed ShopWise score"]) + "."
    return Recommendation(product=product, why=why, labels=["Best Overall", "Evidence-backed"])
