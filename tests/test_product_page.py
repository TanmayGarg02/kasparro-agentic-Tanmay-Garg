import json

def test_product_page_output():
    with open("outputs/product_page.json") as f:
        page = json.load(f)
    assert "product_name" in page
    assert "price" in page
