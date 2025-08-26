import google.generativeai as genai
import re, ast
from decouple import config

genai.configure(api_key=config("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def order_resume_into_dictionary_LLM(raw_text: str):
    prompt = f"""
    You are a resume parser. Your job is to extract structured data from raw resume text and return it as a valid **Python dictionary** (not JSON).

    Use the following schema:

    - `name`: Full name at the top.
    - `title`: Job title directly under the name.
    - `summary`: Paragraph before the WORK EXPERIENCE section.
    - `work_experience`: a list of entries. Each entry must include all of these keys (even if the value is missing, use "". Never use None):
        {{
        "position": str (use empty string `""` if missing),
        "company": str (use empty string `""` if missing),
        "start month": str (use empty string `""` if missing),
        "start year": int or `""` (if unknown),
        "end month": str (use empty string `""` if missing),
        "end year": int, "Present", or `""` (if unknown),
        "description": list of bullet points (can be empty)
        }}
    - `education`: A single multi-line string containing all education-related information.
    - `skills`: A flat list of all skills found (ignore categories like "Technical Skills" — just extract the items).
    - `contact`: A dictionary with only the keys found in the text. Valid keys:
        - `location`
        - `phone`
        - `email`
        - `linkedin`
        - `github`

        Omit any contact field that is missing. Do **not** use null or None in contact fields.

    - `other`: A list of any information that does not fit in the above sections (certifications, references, tips, etc.).

    Instructions:
    - Do not fabricate any content.
    - If any value is missing or unknown, use `""` or `[]`, not `None` or `null`.
    - For dates, extract the month and year if available.
    - If an end date is missing or the job is ongoing, use `"end month": ""` and `"end year": "Present"`.
    - Remove all newline characters (`\\n`) **inside** text values by replacing them with a single space, so that sentences and bullet points are continuous and clean.
    - Preserve line breaks only between list items or sections, but do not include `\\n` inside individual strings.
    - ONLY output a single Python dictionary literal. Do NOT include any code, functions, explanations, or comments.
    Here is the resume text:
    {raw_text}
    """
    response = model.generate_content(prompt)
    
    # Clean triple backticks and whitespace
    text = re.sub(r"^```(?:python)?\s*", "", response.text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    # Remove variable assignment if present, e.g. "resume_data = {...}"
    match = re.match(r'^\s*\w+\s*=\s*(\{.*\})\s*$', text, re.DOTALL)
    if match:
        text = match.group(1)

    # Now safely parse dictionary literal
    return ast.literal_eval(text.strip())
