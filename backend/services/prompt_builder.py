def build_comparison_prompt(resume_text: str, job_description_text: str) -> str:
    prompt = f"""You are an expert technical recruiter and resume analyst.

Compare the RESUME below against the JOB DESCRIPTION below, and evaluate how well the resume matches the job requirements.

RESUME:
\"\"\"
{resume_text}
\"\"\"

JOB DESCRIPTION:
\"\"\"
{job_description_text}
\"\"\"

Respond with ONLY a valid JSON object, and nothing else. Do not include any explanation, markdown formatting, or code fences. The JSON object must exactly follow this structure:

{{
  "match_score": <integer between 0 and 100>,
  "missing_keywords": [<list of important skills/keywords from the job description that are missing or weak in the resume>],
  "suggestions": [<list of specific, actionable rewrite suggestions to improve the resume for this job>]
}}

Rules:
- match_score must be an integer from 0 to 100 reflecting overall fit.
- missing_keywords should contain only meaningful skills, tools, or qualifications, not generic words.
- suggestions should be specific and actionable, referencing the resume content directly.
- Return ONLY the JSON object. No preamble, no extra text, no markdown code fences.
"""
    return prompt