from backend.agents.requirement_parser import parse_requirements
from backend.models.product import ResearchResult
from backend.services.product_service import evidence_to_products


def test_source_image_url_is_preserved_on_product():
    requirements = parse_requirements("Find the best phone under ₹50,000")
    result = ResearchResult(
        title="Samsung Galaxy S24",
        url="https://retailer.example/p/samsung-galaxy-s24",
        content="Samsung Galaxy S24 smartphone ₹49,999 camera battery",
        image_url="https://cdn.example/images/galaxy-s24.jpg",
        purpose="product discovery",
    )
    products = evidence_to_products([result], requirements)
    assert products[0].image_url == "https://cdn.example/images/galaxy-s24.jpg"
