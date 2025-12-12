from core.orchestrator import run_orchestration
import json

def test_question_generation():
    output = run_orchestration("data/product.json")
    with open("outputs/faq.json") as f:
        faq = json.load(f)
    assert len(faq["faqs"]["question_list"]) > 0
