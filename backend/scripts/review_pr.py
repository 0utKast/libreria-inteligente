import os
import sys
import json
import traceback
from google import genai # Changed import

def review_pull_request(pr_diff: str):
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("No se encontró la variable de entorno GOOGLE_API_KEY ni GEMINI_API_KEY.")
    # genai.configure(api_key=api_key) # Removed this line

    try:
        client = genai.Client(api_key=api_key) # Instantiate client with API key
        # model = client.get_model('gemini-1.5-pro-latest') # Incorrect way to get model

        prompt = f"""Revisa el siguiente diff de Pull Request en busca de problemas de calidad de código, estilo, posibles errores, y sugerencias de mejora. Proporciona tu retroalimentación en un formato conciso y claro, utilizando Markdown.

Diff de la Pull Request:
```diff
{pr_diff}
```
"""
        response = client.models.generate_content(model='gemini-1.5-pro-latest', contents=prompt)
        review_text = response.text
        print(json.dumps({"review": review_text}))

    except Exception as e:
        error_traceback = traceback.format_exc()
        error_output = {"error": str(e), "traceback": error_traceback, "raw_response": response.text if 'response' in locals() else "No response"}
        print(json.dumps(error_output), file=sys.stderr)
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(1)

if __name__ == "__main__":
    pr_diff_content = sys.stdin.read()
    review_pull_request(pr_diff_content)
