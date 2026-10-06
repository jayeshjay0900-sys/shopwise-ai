from backend.agents.requirement_parser import parse_requirements


def test_extracts_laptop_budget_and_ml_requirements():
    result = parse_requirements("I need a laptop under ₹1 lakh for AI and machine learning with NVIDIA and 16GB RAM")
    assert result.category == "Laptop"
    assert result.budget == 100000
    assert result.use_case == "AI / Machine Learning"
    assert "NVIDIA" in result.preferences
    assert "16GB RAM" in result.must_have


def test_follow_up_reuses_previous_constraints():
    previous = parse_requirements("best gaming laptop under ₹100000")
    result = parse_requirements("Which is best for deep learning?", previous)
    assert result.budget == 100000
    assert result.category == "Laptop"
    assert result.use_case == "AI / Machine Learning"
