# agents/product_page_agent.py

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path
import json
import re
from core.models import Product, ProductPage

class ProductPageAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            api_key=api_key
        )

        template = Path("templates/product_page_template.txt").read_text()

        self.prompt = PromptTemplate(
            template=template,
            input_variables=["product_json"]
        )

    def build_page(self, product: Product) -> ProductPage:
        chain = self.prompt | self.llm | StrOutputParser()
        product_json_str = product.model_dump_json(indent=2)

        result = chain.invoke({"product_json": product_json_str})

        match = re.search(r'\{.*\}', result, re.DOTALL)
        if not match:
            raise ValueError("Could not find a JSON object in the response")

        # Validate the data with the Pydantic model
        page_data = json.loads(match.group(0))
        return ProductPage(**page_data)
