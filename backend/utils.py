import os
import google.generativeai as genai
from dotenv import load_dotenv

def configure_genai():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la API Key. Asegúrate de que GOOGLE_API_KEY o GEMINI_API_KEY estén configuradas en tu archivo .env")
    genai.configure(api_key=api_key)