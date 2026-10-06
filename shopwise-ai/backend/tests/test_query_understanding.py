from backend.agents.requirement_parser import parse_requirements


def test_structured_llm_understands_macbooks_without_inventing_budget():
    result = parse_requirements("apple macbooks", structured={"category": "laptop", "brand": "Apple", "product_family": "MacBook", "budget_max": None, "currency": "INR"})
    assert result.category == "Laptop"
    assert result.brand == "Apple"
    assert result.model_family == "MacBook"
    assert result.budget is None


def test_structured_llm_keeps_explicit_loq_budget():
    result = parse_requirements("best LOQ laptops under 2 lakhs", structured={"category": "laptop", "brand": "Lenovo", "product_family": "LOQ", "budget_max": 200000, "currency": "INR"})
    assert result.brand == "Lenovo"
    assert result.model_family == "LOQ"
    assert result.budget == 200000
