import os
import sys
import json
import traceback
import google.generativeai as genai

def review_pull_request(pr_diff_file_path: str):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    try:
        with open(pr_diff_file_path, 'r', encoding='utf-8') as f:
            pr_diff = f.read()

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
        print(json.dumps(error_output))
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        error_output = {"error": "Usage: python review_pr.py <pr_diff_file_path>"}
        print(json.dumps(error_output))
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(1)
    
    pr_diff_file_path_arg = sys.argv[1]
    review_pull_request(pr_diff_file_path_arg)
