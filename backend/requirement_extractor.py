import re
from typing import Optional, Tuple, List
from models import Requirement


class RequirementExtractor:
    """Extract and parse shopping requirements from natural language queries"""

    # Indian currency patterns
    CURRENCY_PATTERNS = [
        (r'₹\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lakh|lakhs?|l)', lambda x: float(x.replace(',', '')) * 100000),
        (r'(\d+(?:\.\d+)?)\s*(?:lakh|lakhs?|l)', lambda x: float(x) * 100000),
        (r'₹\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*k', lambda x: float(x.replace(',', '')) * 1000),
        (r'(\d+(?:\.\d+)?)\s*k', lambda x: float(x) * 1000),
        (r'₹\s*(\d+(?:,\d+)*(?:\.\d+)?)', lambda x: float(x.replace(',', ''))),
    ]

    # Comparison indicators
    COMPARISON_KEYWORDS = ['vs', 'versus', 'compare', 'or', 'between']

    # Product categories
    CATEGORIES = {
        'laptop': ['laptop', 'notebook', 'macbook'],
        'phone': ['phone', 'mobile', 'smartphone', 'iphone'],
        'tablet': ['tablet', 'ipad'],
        'headphone': ['headphone', 'headset', 'earphone', 'earbud', 'airpod'],
        'watch': ['watch', 'smartwatch'],
        'camera': ['camera', 'dslr', 'mirrorless'],
    }

    # Common brands
    BRANDS = [
        'apple', 'samsung', 'lenovo', 'dell', 'hp', 'asus', 'acer',
        'msi', 'alienware', 'razer', 'microsoft', 'google', 'oneplus',
        'xiaomi', 'realme', 'oppo', 'vivo', 'nothing', 'sony', 'jbl',
        'bose', 'logitech', 'corsair', 'hyperx', 'steelseries',
    ]

    def extract(self, query: str) -> Requirement:
        """Extract requirements from query"""
        query_lower = query.lower().strip()

        # Check for comparison mode
        comparison_mode, comparison_products = self._detect_comparison(query_lower)

        # Extract category
        category = self._extract_category(query_lower)

        # Extract brand and model
        brand, model_family = self._extract_brand_model(query, query_lower)

        # Extract budget (CRITICAL: only if explicitly mentioned)
        budget_min, budget_max = self._extract_budget(query_lower)

        # Extract use case and features
        use_case, must_have_features = self._extract_features(query_lower)

        return Requirement(
            category=category,
            brand=brand,
            model_family=model_family,
            budget_min=budget_min,
            budget_max=budget_max,
            must_have_features=must_have_features,
            use_case=use_case,
            comparison_mode=comparison_mode,
            comparison_products=comparison_products,
        )

    def _detect_comparison(self, query_lower: str) -> Tuple[bool, List[str]]:
        """Detect if query is a comparison request"""
        for keyword in self.COMPARISON_KEYWORDS:
            if keyword in query_lower:
                # Try to extract product names
                parts = re.split(r'\s+(?:vs|versus|or|compare|between)\s+', query_lower)
                if len(parts) >= 2:
                    products = [p.strip() for p in parts if p.strip()]
                    return True, products
        return False, []

    def _extract_category(self, query_lower: str) -> Optional[str]:
        """Extract product category"""
        for category, keywords in self.CATEGORIES.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        return None

    def _extract_brand_model(self, query: str, query_lower: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract brand and model family"""
        brand = None
        model_family = None

        # Check for brands (case-insensitive)
        for b in self.BRANDS:
            if b in query_lower:
                brand = b.title()
                break

        # Extract model families (case-sensitive for acronyms)
        # Look for common patterns like "LOQ", "MacBook", "iPhone", "Galaxy"
        model_patterns = [
            r'\b(MacBook(?:\s+(?:Pro|Air))?)\b',
            r'\b(iPhone\s*\d*\s*(?:Pro|Max|Plus)?)\b',
            r'\b(Galaxy\s*[A-Z]\d+)\b',
            r'\b(LOQ)\b',
            r'\b(ThinkPad)\b',
            r'\b(Inspiron)\b',
            r'\b(Pavilion)\b',
            r'\b(ROG)\b',
            r'\b(Predator)\b',
            r'\b(Legion)\b',
        ]

        for pattern in model_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                model_family = match.group(1)
                break

        return brand, model_family

    def _extract_budget(self, query_lower: str) -> Tuple[Optional[float], Optional[float]]:
        """
        Extract budget from query.
        CRITICAL: Only extract if explicitly mentioned.
        Return None if no budget mentioned (e.g., "apple macbooks")
        """
        budget_min = None
        budget_max = None

        # Check for "under X" pattern
        under_pattern = r'(?:under|below|less than|within|up to)\s+'
        for pattern, converter in self.CURRENCY_PATTERNS:
            match = re.search(under_pattern + pattern, query_lower)
            if match:
                budget_max = converter(match.group(1))
                return budget_min, budget_max

        # Check for "above X" pattern
        above_pattern = r'(?:above|over|more than)\s+'
        for pattern, converter in self.CURRENCY_PATTERNS:
            match = re.search(above_pattern + pattern, query_lower)
            if match:
                budget_min = converter(match.group(1))
                return budget_min, budget_max

        # Check for range "X to Y" or "between X and Y"
        for pattern1, converter1 in self.CURRENCY_PATTERNS:
            for pattern2, converter2 in self.CURRENCY_PATTERNS:
                range_pattern = f'{pattern1}\\s*(?:to|-|and)\\s*{pattern2}'
                match = re.search(range_pattern, query_lower)
                if match:
                    budget_min = converter1(match.group(1))
                    budget_max = converter2(match.group(2))
                    return budget_min, budget_max

        # Check for standalone amount (only if combined with "budget" or "price")
        if any(word in query_lower for word in ['budget', 'price', 'cost']):
            for pattern, converter in self.CURRENCY_PATTERNS:
                match = re.search(pattern, query_lower)
                if match:
                    budget_max = converter(match.group(1))
                    return budget_min, budget_max

        # No budget mentioned - return None
        return None, None

    def _extract_features(self, query_lower: str) -> Tuple[Optional[str], List[str]]:
        """Extract use case and must-have features"""
        use_case = None
        must_have_features = []

        # Use cases
        use_case_patterns = {
            'gaming': ['gaming', 'games', 'gamer'],
            'coding': ['coding', 'programming', 'development', 'developer'],
            'video editing': ['video editing', 'editing', 'content creation'],
            'photography': ['photography', 'camera', 'photo'],
            'business': ['business', 'office', 'work'],
            'student': ['student', 'study', 'college'],
        }

        for uc, keywords in use_case_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                use_case = uc
                break

        # Features
        feature_keywords = {
            'lightweight': ['lightweight', 'light', 'portable', 'thin'],
            'long battery': ['battery', 'battery life'],
            'good display': ['display', 'screen', 'oled', 'amoled', '4k', 'retina'],
            'powerful': ['powerful', 'performance', 'fast', 'speed'],
            'good camera': ['camera'],
            '5g': ['5g'],
            'touchscreen': ['touchscreen', 'touch screen'],
            'ssd': ['ssd', 'nvme'],
            'dedicated gpu': ['gpu', 'graphics', 'rtx', 'gtx', 'radeon'],
        }

        for feature, keywords in feature_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                must_have_features.append(feature)

        return use_case, must_have_features
