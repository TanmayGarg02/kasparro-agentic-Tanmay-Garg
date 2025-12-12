# agents/faq_agent.py

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path
import json
import re
from core.models import Product, FAQOutput

class FAQAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            api_key=api_key
        )

        template_str = Path("templates/faq_template.txt").read_text()

        self.prompt = PromptTemplate(
            template=template_str,
            input_variables=["product_json", "questions", "product_name"]
        )

        self.parser = StrOutputParser()

    def build_faq(self, product: Product, questions: list[str], product_name: str = None) -> FAQOutput:
        product_json_str = product.model_dump_json(indent=2)
        product_name = product_name or product.product_name

        chain = self.prompt | self.llm | self.parser

        result = chain.invoke({
            "product_json": product_json_str,
            "questions": questions,
            "product_name": product_name
        })

        match = re.search(r'\{.*\}', result, re.DOTALL)
        if not match:
            raise ValueError("Could not find a JSON object in the response")

        # Validate the data with the Pydantic model
        faq_data = json.loads(match.group(0))
        return FAQOutput(**faq_data)
