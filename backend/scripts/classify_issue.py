import os
import sys
import json
import traceback
import google.generativeai as genai

def classify_issue(title: str, body: str):
    print(f"DEBUG: Initializing Gemini API with key: {os.environ.get("GEMINI_API_KEY")[:5]}...", file=sys.stderr)
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Clasifica la siguiente incidencia de GitHub. Devuelve la respuesta en formato JSON con las claves 'label' (ej. 'bug', 'feature', 'documentation', 'enhancement') y 'priority' (ej. 'low', 'medium', 'high', 'critical').

Título: {title}
Cuerpo: {body}
"""
    print(f"DEBUG: Prompting Gemini with: {prompt}", file=sys.stderr)

    try:
        print("DEBUG: Calling model.generate_content...", file=sys.stderr)
        response = model.generate_content(prompt)
        print("DEBUG: model.generate_content call completed.", file=sys.stderr)
        print(f"DEBUG: Raw Gemini response: {response.text}", file=sys.stderr)
        # Asumimos que la respuesta de Gemini es un JSON válido directamente o está dentro de un bloque de código
        # Si Gemini envuelve el JSON en markdown, necesitamos extraerlo
        text_response = response.text.replace('```json', '').replace('```', '').strip()
        print(f"DEBUG: Cleaned Gemini response: {text_response}", file=sys.stderr)
        classification = json.loads(text_response)
        print(json.dumps(classification))
    except Exception as e:
        error_traceback = traceback.format_exc()
        error_output = {"error": str(e), "traceback": error_traceback, "raw_response": response.text if 'response' in locals() else "No response"}
        print(json.dumps(error_output))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        error_output = {"error": "Usage: python classify_issue.py <issue_title> <issue_body>"}
        print(json.dumps(error_output))
        sys.exit(1)
    
    issue_title = sys.argv[1]
    issue_body = sys.argv[2]
    
    classify_issue(issue_title, issue_body)
