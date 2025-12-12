# core/orchestrator.py

from pathlib import Path
import json
import os
from dotenv import load_dotenv

load_dotenv()

from core.models import Product
from agents.faq_agent import FAQAgent
from agents.product_page_agent import ProductPageAgent
from agents.comparison_agent import ComparisonAgent
from agents.question_agent import QuestionGeneratorAgent


class Writer:
    def __init__(self, output_dir="outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def write(self, filename: str, data: dict):
        with open(self.output_dir / filename, "w") as f:
            json.dump(data, f, indent=4)


class Orchestrator:
    def __init__(self, data_path="data/product.json"):
        self.data_path = Path(data_path)

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in environment")

        self.question_agent = QuestionGeneratorAgent(api_key)
        self.faq_agent = FAQAgent(api_key)
        self.page_agent = ProductPageAgent(api_key)
        self.compare_agent = ComparisonAgent(api_key)

    def load_product(self) -> Product:
        data = json.loads(self.data_path.read_text())
        return Product(**data)

    def run(self):
        product = self.load_product()

        question_model = self.question_agent.generate_questions(product)

        faq = self.faq_agent.build_faq(product, question_model.questions)
        page = self.page_agent.build_page(product)
        compare = self.compare_agent.compare(product)

        return {
            "questions": question_model.model_dump(),
            "faq": faq.model_dump(),
            "product_page": page.model_dump(),
            "comparison": compare.model_dump(),
        }


def run_orchestration(input_path: str):
    orchestrator = Orchestrator(input_path)
    result = orchestrator.run()

    writer = Writer()
    writer.write("faq.json", result["faq"])
    writer.write("product_page.json", result["product_page"])
    writer.write("comparison_page.json", result["comparison"])

    return result
