from core.models import Product
import pytest

def test_invalid_product():
    with pytest.raises(Exception):
        Product(product_name="A", concentration="x", skin_type="wrong")
