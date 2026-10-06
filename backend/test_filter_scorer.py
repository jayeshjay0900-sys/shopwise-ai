import pytest
from models import ProductEvidence, Requirement
from product_filter import ProductFilter


class TestProductFilter:
    """Test hard filtering logic"""

    def setup_method(self):
        self.filter = ProductFilter()

    def test_filter_by_brand(self):
        """Test brand filtering"""
        products = [
            ProductEvidence(name="Apple MacBook Pro", price=150000, url="http://test.com", source="test"),
            ProductEvidence(name="Dell XPS 15", price=140000, url="http://test.com", source="test"),
            ProductEvidence(name="Lenovo ThinkPad", price=130000, url="http://test.com", source="test"),
        ]

        req = Requirement(brand="Apple")
        filtered = self.filter.filter(products, req)

        assert len(filtered) == 1
        assert "Apple" in filtered[0].name

    def test_filter_by_model(self):
        """Test model family filtering"""
        products = [
            ProductEvidence(name="Lenovo LOQ 15", price=120000, url="http://test.com", source="test"),
            ProductEvidence(name="Lenovo IdeaPad", price=80000, url="http://test.com", source="test"),
            ProductEvidence(name="Dell Inspiron", price=70000, url="http://test.com", source="test"),
        ]

        req = Requirement(model_family="LOQ")
        filtered = self.filter.filter(products, req)

        assert len(filtered) == 1
        assert "LOQ" in filtered[0].name

    def test_filter_by_budget_max(self):
        """Test maximum budget filtering"""
        products = [
            ProductEvidence(name="Product A", price=50000, url="http://test.com", source="test"),
            ProductEvidence(name="Product B", price=100000, url="http://test.com", source="test"),
            ProductEvidence(name="Product C", price=150000, url="http://test.com", source="test"),
        ]

        req = Requirement(budget_max=100000)
        filtered = self.filter.filter(products, req)

        assert len(filtered) == 2
        assert all(p.price <= 100000 for p in filtered)

    def test_filter_by_budget_min(self):
        """Test minimum budget filtering"""
        products = [
            ProductEvidence(name="Product A", price=50000, url="http://test.com", source="test"),
            ProductEvidence(name="Product B", price=100000, url="http://test.com", source="test"),
            ProductEvidence(name="Product C", price=150000, url="http://test.com", source="test"),
        ]

        req = Requirement(budget_min=80000)
        filtered = self.filter.filter(products, req)

        assert len(filtered) == 2
        assert all(p.price >= 80000 for p in filtered)

    def test_filter_by_budget_range(self):
        """Test budget range filtering"""
        products = [
            ProductEvidence(name="Product A", price=50000, url="http://test.com", source="test"),
            ProductEvidence(name="Product B", price=100000, url="http://test.com", source="test"),
            ProductEvidence(name="Product C", price=150000, url="http://test.com", source="test"),
        ]

        req = Requirement(budget_min=60000, budget_max=120000)
        filtered = self.filter.filter(products, req)

        assert len(filtered) == 1
        assert filtered[0].price == 100000

    def test_filter_rejects_no_price_when_budget_specified(self):
        """Test that products without prices are rejected when budget is specified"""
        products = [
            ProductEvidence(name="Product A", price=50000, url="http://test.com", source="test"),
            ProductEvidence(name="Product B", price=None, url="http://test.com", source="test"),
        ]

        req = Requirement(budget_max=100000)
        filtered = self.filter.filter(products, req)

        assert len(filtered) == 1
        assert filtered[0].price is not None

    def test_no_budget_keeps_all_products(self):
        """Test that no budget constraint keeps all products"""
        products = [
            ProductEvidence(name="Product A", price=50000, url="http://test.com", source="test"),
            ProductEvidence(name="Product B", price=None, url="http://test.com", source="test"),
            ProductEvidence(name="Product C", price=200000, url="http://test.com", source="test"),
        ]

        req = Requirement()  # No budget
        filtered = self.filter.filter(products, req)

        assert len(filtered) == 3

    def test_combined_filters(self):
        """Test multiple filters together"""
        products = [
            ProductEvidence(name="Apple MacBook Pro", price=150000, url="http://test.com", source="test"),
            ProductEvidence(name="Apple MacBook Air", price=90000, url="http://test.com", source="test"),
            ProductEvidence(name="Dell XPS", price=80000, url="http://test.com", source="test"),
        ]

        req = Requirement(brand="Apple", budget_max=100000)
        filtered = self.filter.filter(products, req)

        assert len(filtered) == 1
        assert filtered[0].name == "Apple MacBook Air"

    def test_filter_returns_empty_when_no_matches(self):
        """Test that empty list is returned when no products match"""
        products = [
            ProductEvidence(name="Dell XPS", price=150000, url="http://test.com", source="test"),
        ]

        req = Requirement(brand="Apple")
        filtered = self.filter.filter(products, req)

        assert len(filtered) == 0


class TestPriceValidation:
    """Test price validation logic"""

    def test_reject_zero_price(self):
        """Test rejection of ₹0"""
        from product_processor import ProductProcessor
        from unittest.mock import Mock

        processor = ProductProcessor(Mock())
        assert processor._is_valid_price(0) is False

    def test_reject_obviously_low_prices(self):
        """Test rejection of ₹1, ₹2, ₹5, ₹10"""
        from product_processor import ProductProcessor
        from unittest.mock import Mock

        processor = ProductProcessor(Mock())
        assert processor._is_valid_price(1) is False
        assert processor._is_valid_price(2) is False
        assert processor._is_valid_price(5) is False
        assert processor._is_valid_price(10) is False

    def test_accept_reasonable_prices(self):
        """Test acceptance of reasonable prices"""
        from product_processor import ProductProcessor
        from unittest.mock import Mock

        processor = ProductProcessor(Mock())
        assert processor._is_valid_price(1000) is True
        assert processor._is_valid_price(50000) is True
        assert processor._is_valid_price(150000) is True

    def test_reject_unreasonably_high_prices(self):
        """Test rejection of unreasonably high prices"""
        from product_processor import ProductProcessor
        from unittest.mock import Mock

        processor = ProductProcessor(Mock())
        assert processor._is_valid_price(200000000) is False

    def test_accept_none_as_invalid(self):
        """Test that None price is invalid"""
        from product_processor import ProductProcessor
        from unittest.mock import Mock

        processor = ProductProcessor(Mock())
        assert processor._is_valid_price(None) is False


class TestProductScoring:
    """Test deterministic scoring"""

    def test_scoring_with_brand_match(self):
        """Test scoring rewards brand match"""
        from product_scorer import ProductScorer

        scorer = ProductScorer()

        product_match = ProductEvidence(
            name="Apple MacBook Pro",
            price=100000,
            url="http://test.com",
            source="test"
        )

        product_no_match = ProductEvidence(
            name="Dell XPS",
            price=100000,
            url="http://test.com",
            source="test"
        )

        req = Requirement(brand="Apple")

        score_match = scorer._calculate_score(product_match, req)
        score_no_match = scorer._calculate_score(product_no_match, req)

        assert score_match > score_no_match

    def test_scoring_with_model_match(self):
        """Test scoring rewards model match"""
        from product_scorer import ProductScorer

        scorer = ProductScorer()

        product = ProductEvidence(
            name="Lenovo LOQ 15",
            price=100000,
            url="http://test.com",
            source="test"
        )

        req_match = Requirement(model_family="LOQ")
        req_no_match = Requirement(model_family="ThinkPad")

        score_match = scorer._calculate_score(product, req_match)
        score_no_match = scorer._calculate_score(product, req_no_match)

        assert score_match > score_no_match

    def test_scoring_with_budget_optimization(self):
        """Test scoring rewards efficient budget use"""
        from product_scorer import ProductScorer

        scorer = ProductScorer()

        req = Requirement(budget_max=100000)

        # Sweet spot: 70-100% of budget
        product_optimal = ProductEvidence(
            name="Product A",
            price=90000,
            url="http://test.com",
            source="test"
        )

        # Too cheap: under 50%
        product_cheap = ProductEvidence(
            name="Product B",
            price=30000,
            url="http://test.com",
            source="test"
        )

        score_optimal = scorer._calculate_score(product_optimal, req)
        score_cheap = scorer._calculate_score(product_cheap, req)

        assert score_optimal > score_cheap

    def test_score_capped_at_100(self):
        """Test that score is capped at 100"""
        from product_scorer import ProductScorer

        scorer = ProductScorer()

        product = ProductEvidence(
            name="Apple MacBook Pro",
            price=90000,
            url="http://amazon.in/test",
            source="amazon.in",
            specifications={"cpu": "M3", "ram": "16GB"}
        )

        req = Requirement(brand="Apple", model_family="MacBook", budget_max=100000)

        score = scorer._calculate_score(product, req)

        assert score <= 100.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
