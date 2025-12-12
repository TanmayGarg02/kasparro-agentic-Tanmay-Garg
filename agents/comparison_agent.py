# agents/comparison_agent.py

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path
import json
import re
import random
from core.models import Product, ComparisonPage

class ComparisonAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            api_key=api_key
        )

        template = Path("templates/comparison_template.txt").read_text()

        self.prompt = PromptTemplate(
            template=template,
            input_variables=["product_a", "product_b"]
        )

    def compare(self, product: Product) -> ComparisonPage:
        product_a_json = product.model_dump_json(indent=2)

        # Generate a more creative fictional competitor
        competitor_names = [
            "Radiant Glow Serum",
            "HydraBoost Elixir",
            "ClearSkin Solution",
            "Youthful Vibe Tonic",
            "PureBalance Formula",
            "Face Serum"
        ]
        competitor_name = random.choice(competitor_names)

        product_b = {
            "product_name": competitor_name,
            "key_ingredients": product.key_ingredients[:],
            "price": (product.price or 500) + 150,
            "benefits": ["Advanced hydration", "All-day moisture", "Silky finish"]
        }

        product_b_json = json.dumps(product_b, indent=2)

        chain = self.prompt | self.llm | StrOutputParser()

        result = chain.invoke({
            "product_a": product_a_json,
            "product_b": product_b_json
        })

        match = re.search(r'\{.*\}', result, re.DOTALL)
        if not match:
            raise ValueError("Could not find a JSON object in the response")

        # Validate the data with the Pydantic model
        comparison_data = json.loads(match.group(0))
        return ComparisonPage(**comparison_data)
