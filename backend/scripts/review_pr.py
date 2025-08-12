import os
import sys
import json
import traceback
import google.generativeai as genai

def review_pull_request(pr_diff: str):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')

        prompt = f"""Revisa el siguiente diff de Pull Request en busca de problemas de calidad de código, estilo, posibles errores, y sugerencias de mejora. Proporciona tu retroalimentación en un formato conciso y claro, utilizando Markdown.

Diff de la Pull Request:
```diff
{pr_diff}
```
"""
        response = model.generate_content(prompt)
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
