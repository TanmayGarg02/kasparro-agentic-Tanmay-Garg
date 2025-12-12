# agents/question_agent.py

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path
import json
import re
from core.models import Product, QuestionList

class QuestionGeneratorAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            api_key=api_key
        )

        template_str = Path("templates/question_template.txt").read_text()

        self.prompt = PromptTemplate(
            template=template_str,
            input_variables=["product_json"]
        )

        self.parser = StrOutputParser()

    def generate_questions(self, product: Product) -> QuestionList:
        product_json_str = product.model_dump_json(indent=2)

        chain = self.prompt | self.llm | self.parser

        result = chain.invoke({"product_json": product_json_str})

        match = re.search(r'\[.*\]', result, re.DOTALL)
        if not match:
            match = re.search(r'\{.*\}', result, re.DOTALL)
            if not match:
                raise ValueError("Could not find a JSON list in the response")

        # The model is expected to return a list of strings.
        # We load it and then validate it with our Pydantic model.
        questions_list = json.loads(match.group(0))
        return QuestionList(questions=questions_list)
