from backend.models.product import Product
from backend.models.search import Requirements
from backend.utils.scoring import score_product


def test_score_rewards_budget_and_required_features():
    product = Product(name="Pro Laptop", brand="Brand", price=80000, specifications={"GPU": "NVIDIA RTX", "RAM": "16GB RAM"}, product_url="https://example.com/product")
    requirements = Requirements(category="Laptop", budget=100000, must_have=["16GB RAM"], preferences=["NVIDIA"], raw_query="laptop")
    score, explanation = score_product(product, requirements)
    assert score >= 70
    assert "within budget" in explanation
