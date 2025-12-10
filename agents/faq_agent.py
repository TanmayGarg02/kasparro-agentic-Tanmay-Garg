# agents/faq_agent.py

import json
import re
import google.generativeai as genai


class FAQAgent:
    def __init__(self, model="models/gemini-2.5-flash"):
        self.model = model

    def clean(self, text: str) -> str:
        text = text.strip()
        text = re.sub(r"^```json\s*", "", text)
        text = re.sub(r"^```\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return text

    def build_faq_prompt(self, product, questions):
        product_name = getattr(product, "product_name", "Product")

        return f"""
You are an expert skincare content generator.  
You must produce a **fully answered FAQ** in clean JSON only.

PRODUCT DETAILS:
{json.dumps(product.dict(), indent=2)}

FAQ QUESTIONS TO ANSWER:
{json.dumps(questions, indent=2)}

TASK:
1. For every question, generate a clear, medically safe and helpful answer.
2. Group questions under sections: Informational, Safety, Usage, Purchase, Comparison.
3. Do NOT leave any answer empty.
4. Return ONLY valid JSON in this exact format:

{{
  "{product_name} FAQs": {{
    "Informational": [ {{ "question": "...", "answer": "..." }} ],
    "Safety": [ {{ "question": "...", "answer": "..." }} ],
    "Usage": [ {{ "question": "...", "answer": "..." }} ],
    "Purchase": [ {{ "question": "...", "answer": "..." }} ],
    "Comparison": [ {{ "question": "...", "answer": "..." }} ]
  }},
  "_meta": {{
    "generated_at": "<ISO timestamp>",
    "version": "1.0"
  }}
}}

Make sure every answer is complete.
No empty strings.
Only JSON.
"""

    def build_faq(self, product, questions):

        prompt = self.build_faq_prompt(product, questions)
        response = genai.GenerativeModel(self.model).generate_content(prompt)

        if not response.text:
            raise ValueError("FAQ agent returned empty output")

        cleaned = self.clean(response.text)

        try:
            parsed = json.loads(cleaned)
            return parsed
        except Exception:
            raise ValueError(f"Response is not valid JSON: {cleaned}")


faq_agent = FAQAgent()
