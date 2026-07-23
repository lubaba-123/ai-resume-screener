import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from services.prompt_builder import build_comparison_prompt

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")


def get_resume_comparison(resume_text: str, job_description_text: str) -> dict:
    prompt = build_comparison_prompt(resume_text, job_description_text)

    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    cleaned_text = raw_text
    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.split("```")[1]
        if cleaned_text.startswith("json"):
            cleaned_text = cleaned_text[4:]
    cleaned_text = cleaned_text.strip()

    parsed = json.loads(cleaned_text)
    return parsed