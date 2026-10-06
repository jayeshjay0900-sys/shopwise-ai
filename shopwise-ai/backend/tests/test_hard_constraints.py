from backend.agents.requirement_parser import parse_requirements
from backend.models.product import ResearchResult
from backend.services.product_service import evidence_to_products, validate_products


def test_explicit_brand_and_family_filter_unrelated_products():
    requirements = parse_requirements("best iPhones under 2 lakh")
    assert requirements.brand == "Apple"
    assert requirements.model_family == "iPhone"
    assert requirements.raw_query == "best iPhones under ₹2,00,000"
    results = [
        ResearchResult(title="Apple iPhone 17 Pro", url="https://retailer.example/p/iphone-17-pro", content="Apple iPhone 17 Pro phone ₹1,49,999", purpose="product discovery"),
        ResearchResult(title="Samsung Galaxy S26 Ultra", url="https://retailer.example/p/galaxy-s26-ultra", content="Samsung Galaxy S26 Ultra phone ₹1,29,999", purpose="product discovery"),
    ]
    products = validate_products(evidence_to_products(results, requirements), requirements)
    assert [product.name for product in products] == ["Apple iPhone 17 Pro"]


def test_corrupted_price_is_not_presented_as_a_real_price():
    requirements = parse_requirements("gaming laptop under 1 lakh")
    result = ResearchResult(title="ASUS TUF Gaming F15", url="https://retailer.example/p/tuf-f15", content="ASUS TUF Gaming F15 laptop ₹2 RTX GPU", purpose="product discovery")
    products = evidence_to_products([result], requirements)
    assert products[0].price is None
