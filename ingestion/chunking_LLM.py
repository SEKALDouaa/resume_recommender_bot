import google.generativeai as genai
from decouple import config

genai.configure(api_key=config("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def generate_deroulement(texte_brut):
    prompt = f"""
    
    """
    response = model.generate_content(prompt)
    return response.text.strip()