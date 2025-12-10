# agents/product_page_agent.py
import json
import re
import google.generativeai as genai

class ProductPageAgent:
    def __init__(self, model="models/gemini-2.5-flash"):
        self.model = model

    def build_page(self, product):
        product_name = getattr(product, "product_name", "Unknown Product")
        prompt = f"Generate complete product page JSON for: {product_name}"

        response = genai.GenerativeModel(self.model).generate_content(prompt)

        text = response.text.strip()

        # Remove triple backticks if present
        text = re.sub(r"^```json\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

        if not text:
            raise ValueError("Received empty response from the model for product page")

        try:
            page_json = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(f"Response is not valid JSON: {text}")

        return page_json
