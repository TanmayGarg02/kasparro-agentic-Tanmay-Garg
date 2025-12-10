# agents/comparison_agent.py

import json
import re
import google.generativeai as genai


class ComparisonAgent:
    def __init__(self, model="models/gemini-2.5-flash"):
        self.model = model

    def build_prompt(self, product, product_b=None):
        """
        Build the prompt used for generating the comparison JSON.
        If product_b is None, the model should invent a realistic competitor.
        """

        product_a_name = getattr(product, "product_name", "Product A")

        if product_b:
            product_b_name = getattr(product_b, "product_name", "Product B")

            return f"""
You are a product comparison engine. Compare these two skincare products and return JSON only.

PRODUCT A:
{json.dumps(product.dict(), indent=2)}

PRODUCT B:
{json.dumps(product_b.dict(), indent=2)}

Return JSON: {{
  "product_a": "...",
  "product_b": "...",
  "similarities": [...],
  "differences": [...],
  "which_is_better_for": {{
      "oily_skin": "...",
      "dry_skin": "...",
      "sensitive_skin": "..."
  }}
}}
""".strip()

        else:
            # No product B, create a competitor yourself
            return f"""
You are a skincare comparison expert. You are given PRODUCT A. 
Generate PRODUCT B yourself as a realistic competitor based on the same category.

PRODUCT A:
{json.dumps(product.dict(), indent=2)}

TASK:
1. Create a fictional PRODUCT B with similar category and target skin types.
2. Then give a structured comparison.

Return JSON only, in this format:

{{
  "product_a": "{product_a_name}",
  "product_b": "Imaginary Competitor Name",
  "competitor_details": {{
      "concentration": "...",
      "skin_type": [...],
      "benefits": [...],
      "price": ...
  }},
  "similarities": [...],
  "differences": [...],
  "which_is_better_for": {{
      "oily_skin": "...",
      "dry_skin": "...",
      "sensitive_skin": "..."
  }}
}}
""".strip()

    def clean_response(self, text: str) -> str:
        """Remove unwanted markdown markers before json.loads."""
        text = text.strip()
        text = re.sub(r"^```json\s*", "", text)
        text = re.sub(r"^```\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()

    def run(self, product, product_b=None):
        prompt = self.build_prompt(product, product_b)
        response = genai.GenerativeModel(self.model).generate_content(prompt)

        if not response.text or response.text.strip() == "":
            raise ValueError("Comparison agent returned empty response")

        cleaned = self.clean_response(response.text)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            raise ValueError(f"Comparison response is not valid JSON: {cleaned}")


comparison_agent = ComparisonAgent()
