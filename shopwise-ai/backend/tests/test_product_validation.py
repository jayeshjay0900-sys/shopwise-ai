import pytest
from pydantic import ValidationError
from backend.models.product import Product
from backend.services.product_service import evidence_to_products
from backend.models.product import ResearchResult
from backend.models.search import Requirements


def test_product_requires_verified_product_url():
    with pytest.raises(ValidationError):
        Product(name="Unknown", product_url="not-a-url")


def test_missing_urls_are_not_returned_as_products():
    requirements = Requirements(category="Phone", product_type="phone", raw_query="phones")
    results = [ResearchResult(title="No link", url="https://example.com/item", content="evidence")]
    products = evidence_to_products(results, requirements)
    assert products == []
