import pytest
from typing import Any, cast

from backend.agents.requirement_parser import parse_requirements
from backend.agents.shopping_agent import ShoppingAgent
from backend.models.product import Evidence, ResearchResult
from backend.models.search import ChatRequest, SearchQuery
from backend.services.product_service import evidence_to_products
from backend.utils.scoring import score_product
from backend.models.product import Product


def test_exact_laptop_query_extracts_all_key_requirements():
    result = parse_requirements("Best laptop under ₹1.2 lakh for AI/ML, data science and gaming, with RTX GPU, 16GB+ RAM, Ryzen 7/Core i7, good cooling and display.")
    assert result.category == "Laptop"
    assert result.product_type == "laptop"
    assert result.budget == 120000
    assert result.use_cases == ["AI / ML", "Data Science", "Gaming"]
    assert "RTX GPU" in result.must_have
    assert "16GB+ RAM" in result.must_have
    assert "Ryzen 7 / Core I7" in result.must_have or "Ryzen 7 / Core i7" in result.must_have
    assert "Good cooling" in result.must_have
    assert "Good display" in result.must_have


def test_article_titles_are_sources_not_products():
    requirements = parse_requirements("Find the best phone under ₹50,000")
    results = [
        ResearchResult(title="Best Mobile Phones under Rs. 50,000 | Buying Guide", url="https://example.com/article/phones", content="Samsung Galaxy S24 and Pixel 8", purpose="product discovery"),
        ResearchResult(title="Samsung Galaxy S24", url="https://retailer.example/p/samsung-galaxy-s24", content="Samsung Galaxy S24 smartphone ₹49,999 camera battery", purpose="product discovery"),
    ]
    products = evidence_to_products(results, requirements)
    assert [product.name for product in products] == ["Samsung Galaxy S24"]
    assert products[0].source_urls == ["https://retailer.example/p/samsung-galaxy-s24"]


@pytest.mark.asyncio
async def test_category_change_discards_previous_products():
    class FakeTavily:
        def build_queries(self, requirements):
            return [SearchQuery(query=requirements.category, purpose="product discovery")]

        async def search(self, query):
            if "Laptop" in query:
                return [ResearchResult(title="ASUS TUF Gaming A15", url="https://retailer.example/p/asus-tuf-a15", content="ASUS TUF Gaming A15 laptop RTX 4060 ₹1,10,000 16GB RAM", purpose="product discovery")]
            return [ResearchResult(title="Samsung Galaxy S24", url="https://retailer.example/p/samsung-galaxy-s24", content="Samsung Galaxy S24 smartphone ₹49,999 camera battery", purpose="product discovery")]

    class FakeLLM:
        async def structured(self, system, user, schema):
            return {}

    agent = ShoppingAgent(tavily=cast(Any, FakeTavily()), llm=cast(Any, FakeLLM()))
    phones = await agent.run(ChatRequest(conversation_id="sequence", message="Find the best phone under ₹50,000 with a great camera and battery."))
    laptops = await agent.run(ChatRequest(conversation_id="sequence", message="Best laptop under ₹1.2 lakh for AI/ML, data science and gaming, with RTX GPU, 16GB+ RAM, Ryzen 7/Core i7, good cooling and display."), phones.requirements, phones.products)
    assert phones.requirements.product_type == "phone"
    assert laptops.requirements.product_type == "laptop"
    assert laptops.products
    assert all(product.product_type == "laptop" for product in laptops.products)
    assert all("Samsung" not in product.name for product in laptops.products)


def test_score_explains_all_requested_requirements():
    product = Product(name="ASUS TUF Gaming A15", category="Laptop", product_type="laptop", price=110000, specifications={"GPU": "RTX 4060", "RAM": "16GB RAM", "CPU": "Ryzen 7", "Cooling": "good cooling", "Display": "good display"}, product_url="https://retailer.example/p/asus-tuf-a15", evidence=[Evidence(title="ASUS TUF Gaming A15", url="https://retailer.example/p/asus-tuf-a15")])
    requirements = parse_requirements("Best laptop under ₹1.2 lakh for AI/ML, data science and gaming, with RTX GPU, 16GB+ RAM, Ryzen 7/Core i7, good cooling and display.")
    score, explanation = score_product(product, requirements)
    assert score > 60
    assert "Requirements: 5/5" in explanation
    assert "Use cases:" in explanation
