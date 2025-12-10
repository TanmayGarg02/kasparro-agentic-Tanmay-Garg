from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Consume the generator to print all model names
for model in genai.list_models():
    print(model)
