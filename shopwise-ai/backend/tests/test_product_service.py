from backend.services.product_service import _price_from_text


def test_price_parser_ignores_malformed_tokens():
    assert _price_from_text("Price ₹") is None
    assert _price_from_text("Price ₹1,299") == 1299
    assert _price_from_text("Price INR 24999.50") == 24999.5
