import json

def test_comparison_page():
    with open("outputs/comparison_page.json") as f:
        comp = json.load(f)
    assert len(comp["similarities"]) >= 1
