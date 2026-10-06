from __future__ import annotations
import re
from backend.models.search import Requirements

CATEGORY_ALIASES = {
    "phone": "Phone", "phones": "Phone", "smartphone": "Phone", "smartphones": "Phone", "iphone": "Phone", "iphones": "Phone",
    "laptop": "Laptop", "laptops": "Laptop", "notebook": "Laptop", "notebooks": "Laptop",
    "headphone": "Headphones", "headphones": "Headphones", "hedphone": "Headphones", "hedphones": "Headphones", "tablet": "Tablet", "tablets": "Tablet",
    "camera": "Camera", "cameras": "Camera", "monitor": "Monitor", "monitors": "Monitor",
}


def _indian_number(value: int) -> str:
    text = str(value)
    if len(text) <= 3: return text
    last, head = text[-3:], text[:-3]
    groups = []
    while head:
        groups.insert(0, head[-2:]); head = head[:-2]
    return ",".join(groups + [last])


def normalize_query(text: str) -> str:
    normalized = re.sub(r"\bi\s+phones?\b", "iPhones", text, flags=re.I)
    for typo, correction in (("gamming", "gaming"), ("hedphones", "headphones"), ("hedphone", "headphone"), ("lack", "lakh"), ("lakhs", "lakh")):
        normalized = re.sub(rf"\b{typo}\b", correction, normalized, flags=re.I)
    normalized = re.sub(r"\biphones\b", "iPhones", normalized, flags=re.I)
    normalized = re.sub(r"\biphone\s*s?\b", "iPhones", normalized, flags=re.I)
    normalized = re.sub(r"\bloq\b", "Lenovo LOQ", normalized, flags=re.I)
    normalized = re.sub(r"\b(under|below|within|upto|up to)\s*([\d.]+)\s*lakhs?\b", lambda match: f"{match.group(1)} ₹{_indian_number(int(float(match.group(2)) * 100000))}", normalized, flags=re.I)
    normalized = re.sub(r"\bunder\s+([\d,]+)\b", lambda match: f"under ₹{_indian_number(int(match.group(1).replace(',', '')))}", normalized, flags=re.I)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def parse_budget(text: str) -> tuple[float | None, str]:
    lakh = re.search(r"(?:under|below|within|upto|up to)\s*₹?\s*([\d.]+)\s*lakh", text, re.I)
    if lakh: return float(lakh.group(1)) * 100000, "INR"
    patterns = [(r"(?:₹|rs\.?|inr)\s*([\d,]+)", "INR"), (r"(?:\$|usd)\s*([\d,]+)", "USD"), (r"(?:under|below|within|upto|up to)\s*(?:₹|rs\.?|inr)?\s*([\d,]+)", "INR")]
    for expression, currency in patterns:
        match = re.search(expression, text, re.I)
        if match: return float(match.group(1).replace(",", "")), currency
    return None, "INR"


def _detect_category(text: str) -> str | None:
    lower = text.lower()
    for alias, category in CATEGORY_ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", lower): return category
    return None


def parse_requirements(text: str, previous: Requirements | None = None, structured: dict | None = None) -> Requirements:
    normalized_text = normalize_query(text)
    budget, currency = parse_budget(normalized_text)
    detected_category = _detect_category(normalized_text)
    category = detected_category or (previous.category if previous else "Not available")
    product_type = category.lower() if category != "Not available" else (previous.product_type if previous else "Not available")
    lower = normalized_text.lower()
    brand = "Apple" if "iphone" in lower else ("Lenovo" if "loq" in lower or "lenovo" in lower else (previous.brand if previous else "Not available"))
    model_family = "iPhone" if "iphone" in lower else ("LOQ" if "loq" in lower else (previous.model_family if previous else "Not available"))
    must_have: list[str] = []
    preferences: list[str] = []
    exclusions = [item.strip() for item in re.findall(r"(?:without|avoid|not)\s+([a-z0-9 -]+)", normalized_text, re.I)]
    if isinstance(structured, dict):
        llm_category = str(structured.get("category") or "").strip().lower()
        llm_brand = str(structured.get("brand") or "").strip()
        llm_family = str(structured.get("product_family") or structured.get("model_family") or "").strip()
        if llm_category in {"phone", "laptop", "headphones", "tablet", "camera", "monitor"} and category == "Not available":
            category, product_type = llm_category.title(), llm_category
        if llm_brand and llm_brand.lower() not in {"none", "null", "not available"}: brand = "Lenovo" if llm_brand.lower() == "lenovo" else ("Apple" if llm_brand.lower() == "apple" else llm_brand)
        if llm_family and llm_family.lower() not in {"none", "null", "not available"}: model_family = llm_family
        structured_budget = structured.get("budget_max")
        if budget is None and isinstance(structured_budget, (int, float)) and structured_budget > 0 and re.search(r"(?:under|below|within|upto|up to|lakh|k|₹|rs\.?|inr|usd|dollar)", normalized_text, re.I):
            budget, currency = float(structured_budget), str(structured.get("currency") or "INR").upper()
        structured_features = structured.get("required_features")
        if isinstance(structured_features, list):
            must_have.extend(str(item).strip() for item in structured_features if str(item).strip())
        excluded = structured.get("excluded_products")
        if isinstance(excluded, list): exclusions.extend(str(item).strip() for item in excluded if str(item).strip())
    use_cases: list[str] = []
    if any(term in lower for term in ["machine learning", "deep learning", "ai/ml", "ai and machine learning", "ai ml"]): use_cases.append("AI / ML")
    if "data science" in lower: use_cases.append("Data Science")
    if "gaming" in lower or "gaming laptop" in lower: use_cases.append("Gaming")
    if "photography" in lower or "camera" in lower: use_cases.append("Photography")
    if not use_cases and previous: use_cases = list(previous.use_cases)
    display_use_cases = ["AI / Machine Learning" if item == "AI / ML" else item for item in use_cases]
    use_case = " / ".join(display_use_cases) if display_use_cases else (previous.use_case if previous else "Not available")
    if re.search(r"\brtx(?:\s*\d{3,4})?\b", lower): must_have.append("RTX GPU")
    ram = re.search(r"(\d+)\s*gb\s*\+?\s*ram", lower)
    if ram: must_have.append(f"{ram.group(1)}GB+ RAM" if "+" in ram.group(0) else f"{ram.group(1)}GB RAM")
    cpu_terms = [term.title() for term in ["ryzen 5", "ryzen 7", "ryzen 9", "core i5", "core i7", "core i9"] if term in lower]
    if cpu_terms: must_have.append(" / ".join(cpu_terms))
    for label, pattern in [("Good cooling", r"good\s+cooling|cooling"), ("Good display", r"good\s+display|great\s+display|\bdisplay\b|oled|high refresh"), ("Great camera", r"great\s+camera|good\s+camera|camera"), ("Good battery", r"good\s+battery|great\s+battery|long battery|battery life")]:
        if re.search(pattern, lower): must_have.append(label)
    for term, label in [("nvidia", "NVIDIA"), ("oled", "OLED"), ("anc", "ANC"), ("5g", "5G")]:
        if term in lower: preferences.append(label)
    explicit_change = bool(previous and detected_category and detected_category != previous.category)
    if previous and not explicit_change:
        must_have = list(dict.fromkeys(previous.must_have + must_have)); preferences = list(dict.fromkeys(previous.preferences + preferences)); exclusions = list(dict.fromkeys(previous.exclusions + exclusions)); use_cases = list(dict.fromkeys(previous.use_cases + use_cases))
    priority = "Performance" if any(term in lower for term in ["gaming", "ai", "machine learning", "data science", "performance"]) else ("Camera" if "camera" in lower else (previous.priority if previous else "Value"))
    comparisons = re.findall(r"(?:compare|vs|versus)\s+(.+)", normalized_text, re.I)
    targets = [item.strip() for item in comparisons[0].split(" and ")] if comparisons else (previous.comparison_targets if previous else [])
    return Requirements(category=category, product_type=product_type, brand=brand, model_family=model_family, budget=budget if budget is not None else (previous.budget if previous else None), currency=currency if budget is not None else (previous.currency if previous else "INR"), use_case=use_case, use_cases=use_cases, priority=priority, must_have=list(dict.fromkeys(must_have)), preferences=list(dict.fromkeys(preferences)), exclusions=exclusions, comparison_targets=targets, raw_query=normalized_text)
