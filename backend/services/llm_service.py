import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from services.prompt_builder import build_comparison_prompt

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")


def _clean_json_text(raw_text: str) -> str:
    cleaned_text = raw_text.strip()
    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.split("```")[1]
        if cleaned_text.startswith("json"):
            cleaned_text = cleaned_text[4:]
    return cleaned_text.strip()


def _validate_result(parsed: dict) -> bool:
    if not isinstance(parsed, dict):
        return False
    required_keys = {"match_score", "missing_keywords", "suggestions"}
    if not required_keys.issubset(parsed.keys()):
        return False
    if not isinstance(parsed["match_score"], int):
        return False
    if not (0 <= parsed["match_score"] <= 100):
        return False
    if not isinstance(parsed["missing_keywords"], list):
        return False
    if not isinstance(parsed["suggestions"], list):
        return False
    return True


def get_resume_comparison(resume_text: str, job_description_text: str) -> dict:
    prompt = build_comparison_prompt(resume_text, job_description_text)

    last_error = None

    for attempt in range(2):
        try:
            response = model.generate_content(prompt)
            raw_text = response.text
            cleaned_text = _clean_json_text(raw_text)
            parsed = json.loads(cleaned_text)

            if _validate_result(parsed):
                return parsed
            else:
                last_error = "LLM response did not match the expected JSON structure."
        except json.JSONDecodeError as e:
            last_error = f"Invalid JSON returned by LLM: {str(e)}"
        except Exception as e:
            last_error = f"LLM call failed: {str(e)}"

    raise ValueError(f"Failed to get a valid response after retries. Last error: {last_error}")