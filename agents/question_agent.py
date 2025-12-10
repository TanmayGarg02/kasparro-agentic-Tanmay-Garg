from google import generativeai as genai
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

from core.models import Product
import json


class QuestionGenerationAgent:
    def __init__(self, model="models/gemini-2.5-flash"):
        self.model = model

    def run(self, product: Product):
        prompt = f"""
        You are an AI system generating customer questions about a skincare product.
        Generate at least 15 questions grouped into categories:
        Informational, Safety, Usage, Purchase, Comparison.

        Product Data:
        {product.model_dump_json()}

        Output JSON ONLY in this structure:
        {{
            "Informational": ["question 1", "question 2", ...],
            "Safety": ["question 1", "question 2", ...],
            "Usage": ["question 1", "question 2", ...],
            "Purchase": ["question 1", "question 2", ...],
            "Comparison": ["question 1", "question 2", ...]
        }}
        """

        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt)
        
        # Extract the text from the response
        response_text = response.text
        
        # Clean the response to ensure it's valid JSON
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        return json.loads(response_text)
