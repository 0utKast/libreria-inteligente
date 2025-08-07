import os
import sys
import json
import google.generativeai as genai

def classify_issue(title: str, body: str):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Clasifica la siguiente incidencia de GitHub. Devuelve la respuesta en formato JSON con las claves 'label' (ej. 'bug', 'feature', 'documentation', 'enhancement') y 'priority' (ej. 'low', 'medium', 'high', 'critical').

Título: {title}
Cuerpo: {body}
"""

    try:
        response = model.generate_content(prompt)
        # Asumimos que la respuesta de Gemini es un JSON válido directamente o está dentro de un bloque de código
        # Si Gemini envuelve el JSON en markdown, necesitamos extraerlo
        text_response = response.text.replace('```json', '').replace('```', '').strip()
        classification = json.loads(text_response)
        print(json.dumps(classification))
    except Exception as e:
        print(json.dumps({"error": str(e), "raw_response": response.text if 'response' in locals() else "No response"}))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python classify_issue.py <issue_title> <issue_body>"}))
        sys.exit(1)
    
    issue_title = sys.argv[1]
    issue_body = sys.argv[2]
    
    classify_issue(issue_title, issue_body)
