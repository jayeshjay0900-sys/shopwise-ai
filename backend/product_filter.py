from typing import List
from models import ProductEvidence, Requirement


class ProductFilter:
    """
    Apply HARD filters BEFORE ranking.
    A product failing a hard requirement must not become a recommendation.
    """

    def filter(self, products: List[ProductEvidence], requirement: Requirement) -> List[ProductEvidence]:
        """Apply all hard filters"""
        filtered = products

        # Filter by brand
        if requirement.brand:
            filtered = self._filter_by_brand(filtered, requirement.brand)

        # Filter by model family
        if requirement.model_family:
            filtered = self._filter_by_model(filtered, requirement.model_family)

        # Filter by budget (CRITICAL: only if budget specified)
        if requirement.budget_max is not None or requirement.budget_min is not None:
            filtered = self._filter_by_budget(
                filtered,
                requirement.budget_min,
                requirement.budget_max
            )

        # Filter by category (if specified and can be validated)
        if requirement.category:
            filtered = self._filter_by_category(filtered, requirement.category)

        return filtered

    def _filter_by_brand(self, products: List[ProductEvidence], brand: str) -> List[ProductEvidence]:
        """Hard filter by brand"""
        brand_lower = brand.lower()
        return [
            p for p in products
            if brand_lower in p.name.lower()
        ]

    def _filter_by_model(self, products: List[ProductEvidence], model: str) -> List[ProductEvidence]:
        """Hard filter by model family"""
        model_lower = model.lower()
        return [
            p for p in products
            if model_lower in p.name.lower()
        ]

    def _filter_by_budget(
        self,
        products: List[ProductEvidence],
        budget_min: float = None,
        budget_max: float = None
    ) -> List[ProductEvidence]:
        """
        Hard filter by budget.
        CRITICAL: Products outside budget must be rejected.
        """
        filtered = []

        for product in products:
            # Skip products without valid prices
            if product.price is None:
                continue

            # Check minimum budget
            if budget_min is not None and product.price < budget_min:
                continue

            # Check maximum budget
            if budget_max is not None and product.price > budget_max:
                continue

            filtered.append(product)

        return filtered

    def _filter_by_category(self, products: List[ProductEvidence], category: str) -> List[ProductEvidence]:
        """
        Soft filter by category (since category detection in product name can be fuzzy).
        Only apply if category keyword is clearly present.
        """
        category_keywords = {
            'laptop': ['laptop', 'notebook', 'macbook'],
            'phone': ['phone', 'iphone', 'mobile'],
            'tablet': ['tablet', 'ipad'],
            'headphone': ['headphone', 'headset', 'earphone', 'earbud'],
            'watch': ['watch'],
            'camera': ['camera'],
        }

        keywords = category_keywords.get(category.lower(), [category.lower()])

        # More lenient category check
        filtered = []
        for product in products:
            product_name_lower = product.name.lower()
            if any(keyword in product_name_lower for keyword in keywords):
                filtered.append(product)

        # If filtering removed everything, return original (category might be implicit)
        return filtered if filtered else products
