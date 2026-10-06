import pytest
from requirement_extractor import RequirementExtractor


class TestRequirementExtractor:
    """Test requirement extraction with all accuracy rules"""

    def setup_method(self):
        self.extractor = RequirementExtractor()

    # Budget parsing tests
    def test_budget_parsing_lakh(self):
        """Test lakh format parsing"""
        req = self.extractor.extract("laptop under 1 lakh")
        assert req.budget_max == 100000
        assert req.budget_min is None

    def test_budget_parsing_lakhs(self):
        """Test lakhs plural format"""
        req = self.extractor.extract("LOQ laptops under 2 lakhs")
        assert req.budget_max == 200000

    def test_budget_parsing_decimal_lakh(self):
        """Test decimal lakh parsing"""
        req = self.extractor.extract("phone under 1.5 lakhs")
        assert req.budget_max == 150000

    def test_budget_parsing_rupee_symbol(self):
        """Test ₹ symbol parsing"""
        req = self.extractor.extract("best phone under ₹50,000")
        assert req.budget_max == 50000

    def test_budget_parsing_k_format(self):
        """Test 'k' format parsing"""
        req = self.extractor.extract("phone under 50k")
        assert req.budget_max == 50000

    def test_budget_parsing_rupee_k(self):
        """Test ₹ with k format"""
        req = self.extractor.extract("laptop under ₹70k")
        assert req.budget_max == 70000

    # No-budget queries (CRITICAL)
    def test_no_budget_apple_macbooks(self):
        """CRITICAL: 'apple macbooks' must have budget=None"""
        req = self.extractor.extract("apple macbooks")
        assert req.budget_max is None
        assert req.budget_min is None
        assert req.brand == "Apple"

    def test_no_budget_generic_brand(self):
        """Test generic brand query without budget"""
        req = self.extractor.extract("dell laptops")
        assert req.budget_max is None
        assert req.budget_min is None
        assert req.brand == "Dell"

    def test_no_budget_model_query(self):
        """Test model-specific query without budget"""
        req = self.extractor.extract("iPhone 15")
        assert req.budget_max is None
        assert req.budget_min is None

    # Brand detection
    def test_brand_detection_apple(self):
        """Test Apple brand detection"""
        req = self.extractor.extract("apple macbooks")
        assert req.brand == "Apple"

    def test_brand_detection_lenovo(self):
        """Test Lenovo brand detection"""
        req = self.extractor.extract("lenovo thinkpad")
        assert req.brand == "Lenovo"

    def test_brand_detection_case_insensitive(self):
        """Test case-insensitive brand detection"""
        req = self.extractor.extract("SAMSUNG phones")
        assert req.brand == "Samsung"

    # Model/family detection
    def test_model_detection_loq(self):
        """Test LOQ model detection"""
        req = self.extractor.extract("LOQ laptops under 2 lakhs")
        assert req.model_family == "LOQ"
        assert req.budget_max == 200000

    def test_model_detection_macbook(self):
        """Test MacBook detection"""
        req = self.extractor.extract("apple macbooks")
        assert req.model_family == "MacBook"

    def test_model_detection_iphone(self):
        """Test iPhone detection"""
        req = self.extractor.extract("iPhone 15 Pro Max")
        assert req.model_family is not None
        assert "iphone" in req.model_family.lower()

    def test_model_detection_galaxy(self):
        """Test Galaxy detection"""
        req = self.extractor.extract("Samsung Galaxy S24")
        assert req.model_family is not None
        assert "galaxy" in req.model_family.lower()

    # Category detection
    def test_category_laptop(self):
        """Test laptop category detection"""
        req = self.extractor.extract("best gaming laptop under 1 lakh")
        assert req.category == "laptop"

    def test_category_phone(self):
        """Test phone category detection"""
        req = self.extractor.extract("best phone for camera under ₹50,000")
        assert req.category == "phone"

    def test_category_macbook_is_laptop(self):
        """Test MacBook is recognized as laptop"""
        req = self.extractor.extract("apple macbooks")
        assert req.category == "laptop"

    # Use case detection
    def test_use_case_gaming(self):
        """Test gaming use case detection"""
        req = self.extractor.extract("best gaming laptop under 1 lakh")
        assert req.use_case == "gaming"

    def test_use_case_coding(self):
        """Test coding use case detection"""
        req = self.extractor.extract("laptop for coding")
        assert req.use_case == "coding"

    def test_use_case_photography(self):
        """Test photography use case detection"""
        req = self.extractor.extract("best phone for camera under ₹50,000")
        assert req.use_case == "photography"

    # Comparison queries
    def test_comparison_vs(self):
        """Test comparison with 'vs'"""
        req = self.extractor.extract("iPhone 17 vs Galaxy S26")
        assert req.comparison_mode is True
        assert len(req.comparison_products) == 2

    def test_comparison_or(self):
        """Test comparison with 'or'"""
        req = self.extractor.extract("MacBook Air or MacBook Pro")
        assert req.comparison_mode is True

    # Combined requirements
    def test_combined_brand_category_budget(self):
        """Test combined brand, category, and budget"""
        req = self.extractor.extract("Dell laptop under 60000")
        assert req.brand == "Dell"
        assert req.category == "laptop"
        assert req.budget_max == 60000

    def test_combined_brand_model_budget(self):
        """Test combined brand, model, and budget"""
        req = self.extractor.extract("Lenovo LOQ under 1.5 lakhs")
        assert req.brand == "Lenovo"
        assert req.model_family == "LOQ"
        assert req.budget_max == 150000

    # Edge cases
    def test_no_requirements(self):
        """Test query with minimal information"""
        req = self.extractor.extract("best laptop")
        assert req.category == "laptop"
        assert req.budget_max is None

    def test_budget_range(self):
        """Test budget range parsing"""
        req = self.extractor.extract("laptop between 50000 and 70000")
        assert req.budget_min == 50000
        assert req.budget_max == 70000

    def test_budget_above(self):
        """Test 'above' budget parsing"""
        req = self.extractor.extract("laptop above 1 lakh")
        assert req.budget_min == 100000
        assert req.budget_max is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
