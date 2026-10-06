from __future__ import annotations

import logging
import re
from collections import OrderedDict
from urllib.parse import urlparse
from typing import Any
from pydantic import ValidationError
from backend.models.product import Evidence, PricePoint, Product, ProductExtraction, ResearchResult
from backend.models.search import Requirements
from backend.utils.validation import clean_url

logger = logging.getLogger("shopwise.products")
ARTICLE_MARKERS = ("best ", "top ", "buying guide", "buying guides", "search results", "category", "list of", "under ", "price list", "full features and specifications")
NON_PRODUCT_PATHS = ("/blog/", "/article", "/reviews", "/review/", "/search", "/category", "/buying-guide")
CATEGORY_TERMS = {"phone": ("phone", "smartphone", "iphone", "galaxy", "pixel"), "laptop": ("laptop", "notebook", "macbook", "thinkpad", "vivobook", "ideapad", "tuf", "rog"), "headphones": ("headphone", "earbud", "airpods", "buds"), "tablet": ("tablet", "ipad", "galaxy tab"), "camera": ("camera", "canon", "nikon", "sony alpha"), "monitor": ("monitor", "display", "ultragear")}
MODEL_PATTERNS = {"phone": r"\b(?:Apple\s+)?iPhone\s+\d{1,2}(?:\s+(?:Pro Max|Pro|Plus|Mini|e))?|\bSamsung\s+Galaxy\s+[A-Z]?\d{1,3}(?:\s+Ultra|\s+Pro)?|\bGoogle\s+Pixel\s+\d{1,2}(?:\s+Pro|\s+XL)?|\bOnePlus\s+\d+[A-Za-z]*", "laptop": r"\b(?:Lenovo\s+LOQ\s+\d+|ASUS\s+(?:TUF|ROG)\s+[A-Za-z0-9-]+|HP\s+Victus\s+\d+|Acer\s+Nitro\s+[A-Za-z0-9-]+|Dell\s+G\d+|Apple\s+MacBook\s+(?:Air|Pro))\b"}


def _identity(title: str, url: str) -> str:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    return re.sub(r"[^a-z0-9]", "", f"{title} {host}".lower())[:110]


def _model_identity(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def deduplicate(results: list[ResearchResult]) -> list[ResearchResult]:
    unique: OrderedDict[str, ResearchResult] = OrderedDict()
    for item in results: unique.setdefault(_identity(item.title, str(item.url)), item)
    return list(unique.values())


def _price_from_text(text: str) -> float | None:
    match = re.search(r"(?:₹|INR|Rs\.?)\s*([\d,]+(?:\.\d+)?)", text, re.I)
    if not match: return None
    try:
        value = float(match.group(1).replace(",", ""))
        return value if value >= 100 else None
    except ValueError: return None


def _is_article(title: str) -> bool:
    lower = title.lower().strip()
    return any(marker in lower for marker in ARTICLE_MARKERS) or lower.endswith((" review", " reviews", " guide"))


def _category_matches(title: str, content: str, requirements: Requirements) -> bool:
    terms = CATEGORY_TERMS.get(requirements.product_type.lower(), (requirements.product_type.lower(),))
    return any(term in f"{title} {content[:1000]}".lower() for term in terms)


def _is_product_page(url: str) -> bool:
    parsed = urlparse(url); path = parsed.path.lower()
    if not parsed.netloc or path in {"", "/"} or any(marker in path for marker in NON_PRODUCT_PATHS): return False
    return any(marker in path for marker in ("/p/", "/dp/", "/product", "/products", "/buy/", "/mobile/", "/laptop/")) or len(path.strip("/").split("/")) >= 2


def _looks_like_model(title: str) -> bool:
    lower = title.lower()
    return not _is_article(title) and len(title.split()) >= 2 and not any(term in lower for term in ("search results", "category page", "buying guide"))


def _constraint_matches(name: str, requirements: Requirements) -> bool:
    lower = name.lower()
    if requirements.brand != "Not available" and requirements.brand.lower() not in lower:
        return False
    if requirements.model_family != "Not available" and requirements.model_family.lower() not in lower:
        return False
    return True


def _model_candidates(result: ResearchResult, requirements: Requirements) -> list[str]:
    pattern = MODEL_PATTERNS.get(requirements.product_type.lower())
    if not pattern: return []
    candidates: list[str] = []
    for match in re.finditer(pattern, result.content, re.I):
        window = result.content[max(0, match.start() - 80):match.end() + 180]
        if _price_from_text(window) is not None or re.search(r"\b(?:gb|mah|camera|processor|display|review|specification)\b", window, re.I):
            candidate = re.sub(r"\s+", " ", match.group(0)).strip()
            if requirements.brand == "Apple" and "apple" not in candidate.lower(): candidate = f"Apple {candidate}"
            if not _constraint_matches(candidate, requirements): continue
            if candidate not in candidates: candidates.append(candidate)
    return candidates[:5]


def _unwrap(data: dict[str, Any]) -> dict[str, Any]:
    for key in ("product", "product_details", "result", "data"):
        value = data.get(key)
        if isinstance(value, dict): return value
    return data


def _number(value: Any, integer: bool = False) -> float | int | None:
    if value is None or isinstance(value, bool): return None
    if isinstance(value, (int, float)): return int(value) if integer else float(value)
    match = re.search(r"\d[\d,]*(?:\.\d+)?", str(value))
    if not match: return None
    try: return int(float(match.group(0).replace(",", ""))) if integer else float(match.group(0).replace(",", ""))
    except ValueError: return None


def _strings(value: Any) -> list[str]:
    if isinstance(value, str): return [part.strip(" •-\t") for part in re.split(r"\n|;", value) if part.strip()][:5]
    if isinstance(value, list): return [str(item.get("text", item.get("name", item))) if isinstance(item, dict) else str(item) for item in value][:5]
    return []


def _specifications(value: Any) -> dict[str, str]:
    if isinstance(value, dict): return {str(key): str(item) for key, item in value.items() if item is not None}
    if isinstance(value, list):
        output: dict[str, str] = {}
        for item in value:
            if isinstance(item, dict):
                key, val = item.get("name") or item.get("key") or item.get("label"), item.get("value") or item.get("text")
                if key and val is not None: output[str(key)] = str(val)
        return output
    return {}


def evidence_to_products(results: list[ResearchResult], requirements: Requirements) -> list[Product]:
    products: list[Product] = []
    for result in deduplicate(results):
        title, url = result.title.strip(), clean_url(str(result.url))
        if not title or not url or not _category_matches(title, result.content, requirements): continue
        names = [title] if _looks_like_model(title) else _model_candidates(result, requirements)
        if names == [title] and requirements.brand == "Apple" and "iphone" in title.lower() and "apple" not in title.lower(): names = [f"Apple {title}"]
        names = [name for name in names if _constraint_matches(name, requirements)]
        if not names or (not _is_product_page(url) and not _model_candidates(result, requirements)): continue
        for name in names:
            price = _price_from_text(f"{name} {result.content}")
            evidence = Evidence(title=title, url=url, source_type=result.purpose, snippet=result.content[:500])
            retailer = urlparse(url).netloc.removeprefix("www.")
            prices = [PricePoint(retailer=retailer, amount=price, currency="INR", url=url if _is_product_page(url) else None)] if price is not None else []
            products.append(Product(name=name, brand=name.split()[0], category=requirements.category, product_type=requirements.product_type, price=price, image_url=result.image_url, product_url=url if _is_product_page(url) else None, source_urls=[url], prices=prices, evidence=[evidence]))
    unique: OrderedDict[str, Product] = OrderedDict()
    for product in products: unique.setdefault(_model_identity(product.name), product)
    return list(unique.values())[:5]


def validate_products(products: list[Product], requirements: Requirements) -> list[Product]:
    valid: list[Product] = []; seen: set[str] = set()
    for product in products:
        identity = _identity(product.name, product.product_url or (product.source_urls[0] if product.source_urls else ""))
        if product.product_type != requirements.product_type or not _constraint_matches(product.name, requirements) or (requirements.budget is not None and product.price is not None and product.price > requirements.budget) or not product.source_urls or not product.evidence or identity in seen or _is_article(product.name): continue
        seen.add(identity); valid.append(product)
    return valid[:5]


def merge_analysis(product: Product, data: dict[str, Any]) -> Product:
    raw = _unwrap(data)
    normalized = {"price": _number(raw.get("price")), "rating": _number(raw.get("rating")), "review_count": _number(raw.get("review_count") or raw.get("reviews"), integer=True), "specifications": _specifications(raw.get("specifications") or raw.get("specs")), "pros": _strings(raw.get("pros")), "cons": _strings(raw.get("cons")), "review_summary": str(raw.get("review_summary") or raw.get("summary") or "Not available")}
    try: extracted = ProductExtraction.model_validate(normalized)
    except ValidationError as exc: logger.warning("Product extraction validation fallback: %s", len(exc.errors())); extracted = ProductExtraction()
    product.price = extracted.price if extracted.price is not None else product.price
    product.rating = extracted.rating if extracted.rating is not None else product.rating
    product.review_count = extracted.review_count if extracted.review_count is not None else product.review_count
    if extracted.specifications: product.specifications = extracted.specifications
    if extracted.pros: product.pros = extracted.pros[:5]
    if extracted.cons: product.cons = extracted.cons[:5]
    if extracted.review_summary != "Not available": product.review_summary = extracted.review_summary
    return product
