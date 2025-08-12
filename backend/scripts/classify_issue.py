import os
import sys
import json
import traceback
from google import genai # Changed import

def classify_issue(title: str, body: str):
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("No se encontró la variable de entorno GOOGLE_API_KEY ni GEMINI_API_KEY.")
    # genai.configure(api_key=api_key) # Removed this line
    print(f"DEBUG: Initializing Gemini API with key: {api_key[:5]}...", file=sys.stderr, flush=True)

    try:
        client = genai.Client(api_key=api_key) # Instantiate client with API key
        print("DEBUG: Attempting to list models to verify API key and connectivity...", file=sys.stderr, flush=True)
        for m in client.models.list(): # New way to list models
            if "generateContent" in m.supported_generation_methods:
                print(f"DEBUG: Found model: {m.name}", file=sys.stderr, flush=True)
                break
        else:
            raise Exception("No models supporting generateContent found. API key or connectivity issue?")
        print("DEBUG: API key and connectivity verified.\n", file=sys.stderr, flush=True) # Added newline for clarity

        # model = client.get_model('gemini-1.5-pro-latest') # Old way to get model

        prompt = f"""Clasifica la siguiente incidencia de GitHub. Devuelve la respuesta en formato JSON con las claves 'label' (ej. 'bug', 'feature', 'documentation', 'enhancement') y 'priority' (ej. 'low', 'medium', 'high', 'critical').

Título: {title}
Cuerpo: {body}
"""
        print(f"DEBUG: Prompting Gemini with: {prompt}", file=sys.stderr, flush=True)

        print("DEBUG: Calling client.models.generate_content...", file=sys.stderr, flush=True) # Changed print
        response = client.models.generate_content(model='gemini-1.5-pro-latest', contents=prompt)

        print("DEBUG: model.generate_content call completed.", file=sys.stderr, flush=True)
        print(f"DEBUG: Raw Gemini response: {response.text}", file=sys.stderr, flush=True)
        # Asumimos que la respuesta de Gemini es un JSON válido directamente o está dentro de un bloque de código
        # Si Gemini envuelve el JSON en markdown, necesitamos extraerlo
        text_response = response.text.replace('```json', '').replace('```', '').strip()
        print(f"DEBUG: Cleaned Gemini response: {text_response}", file=sys.stderr, flush=True)
        classification = json.loads(text_response)
        print(json.dumps(classification))
    except Exception as e:
        error_traceback = traceback.format_exc()
        error_output = {"error": str(e), "traceback": error_traceback, "raw_response": response.text if 'response' in locals() else "No response"}
        print(json.dumps(error_output))
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        error_output = {"error": "Usage: python classify_issue.py <issue_title> <issue_body>"}
        print(json.dumps(error_output))
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(1)
    
    issue_title = sys.argv[1]
    issue_body = sys.argv[2]
    
    classify_issue(issue_title, issue_body)
