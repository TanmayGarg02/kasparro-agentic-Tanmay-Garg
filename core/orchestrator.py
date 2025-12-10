# core/orchestrator.py
import json
from pathlib import Path
from typing import Dict, Any

from core.models import Product
from core.writer import write_all
from agents.question_agent import QuestionGenerationAgent
from agents.faq_agent import FAQAgent
from agents.product_page_agent import ProductPageAgent
from agents.comparison_agent import comparison_agent

DATA_PATH = Path("data/product.json")


class Orchestrator:
    def __init__(self, model="models/gemini-2.5-flash"):
        self.model_name = model
        self.question_agent = QuestionGenerationAgent(model=self.model_name)
        self.faq_agent = FAQAgent(model=self.model_name)
        self.product_agent = ProductPageAgent(model=self.model_name)
        self.comparison_agent = comparison_agent

    def load_product(self) -> Product:
        raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        product = Product(**raw)
        return product

    def run(self) -> Dict[str, Any]:
        product = self.load_product()

        # 1. generate questions
        questions = self.question_agent.run(product)

        # 2. build FAQ using selected questions and product blocks
        faq_obj = self.faq_agent.build_faq(product, questions)

        # 3. build product page JSON
        product_page_obj = self.product_agent.build_page(product)

        # 4. build deterministic comparison (with imaginary product B)
        comparison_obj = self.comparison_agent.run(product, product_b=None)

        # 5. write outputs
        paths = write_all(faq_obj, product_page_obj, comparison_obj)

        return {
            "status": "success",
            "paths": paths,
            "summary": {
                "questions_count": sum(len(v) for v in questions.values()) if isinstance(questions, dict) else None
            }
        }


def main():
    orchestrator = Orchestrator()
    result = orchestrator.run()
    print("Orchestration complete")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
