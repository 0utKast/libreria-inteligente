import os
import sys
import google.generativeai as genai
import pathlib

# --- Configuration ---
try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError:
    sys.exit("Error: GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=GEMINI_API_KEY)

project_root = pathlib.Path(__file__).parent.parent.parent

# --- Prompt Templates ---

def get_pytest_prompt(file_content, file_path):
    return f"""
Actúa como un ingeniero de software experto en Python y `pytest`.

He modificado el siguiente archivo de Python: `{file_path}`

Contenido del archivo:
```python
{file_content}
```

Tu tarea es escribir un conjunto de pruebas unitarias exhaustivas para este archivo usando el framework `pytest`.

Requisitos:
1.  Crea mocks para cualquier dependencia externa o llamadas a la base de datos para asegurar que las pruebas sean unitarias y aisladas.
2.  Cubre los casos de uso comunes y el "happy path".
3.  Incluye pruebas para casos límite (edge cases), como entradas vacías, valores nulos o formatos inesperados.
4.  Añade pruebas para el manejo de errores y excepciones.
5.  Asegúrate de que el código de prueba sea limpio, legible y siga las buenas prácticas.
6.  Devuelve únicamente el código de Python para el archivo de prueba. No incluyas explicaciones, solo el código.
"""

def get_jest_prompt(file_content, file_path):
    return f"""
Actúa como un ingeniero de frontend experto en JavaScript y el framework `Jest`.

He modificado el siguiente componente de React: `{file_path}`

Contenido del archivo:
```javascript
{file_content}
```

Tu tarea es escribir un conjunto de pruebas unitarias exhaustivas para este componente usando `Jest` y `React Testing Library`.

Requisitos:
1.  Crea mocks para las llamadas a la API (`fetch`) o cualquier otra función externa para aislar el componente.
2.  Prueba que el componente se renderiza correctamente (pruebas de humo).
3.  Simula eventos de usuario (clics, escritura en campos de texto) y verifica que el estado del componente y el DOM se actualizan como se espera.
4.  Cubre casos límite, como props vacías o con formatos inesperados.
5.  Verifica que los elementos correctos se muestran u ocultan según el estado y las props.
6.  Devuelve únicamente el código de JavaScript para el archivo de prueba (`*.test.js`). No incluyas explicaciones, solo el código.
"""

# --- Main Logic ---

def generate_test_file(file_path_str):
    file_path = pathlib.Path(file_path_str)
    if not file_path.is_file():
        print(f"Skipping: {file_path_str} is not a file or does not exist.")
        return

    print(f"Processing file: {file_path_str}")
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file {file_path_str}: {e}")
        return

    output_path = None
    prompt = None

    # Determine prompt and output path based on file type
    if file_path.suffix == ".py" and "backend" in file_path.parts:
        prompt = get_pytest_prompt(content, file_path_str)
        # Example: backend/crud.py -> backend/tests/test_crud.py
        test_dir = project_root / "backend" / "tests"
        output_path = test_dir / f"test_{file_path.name}"
    elif file_path.suffix == ".js" and "frontend" in file_path.parts:
        prompt = get_jest_prompt(content, file_path_str)
        # Example: frontend/src/App.js -> frontend/src/App.test.js
        output_path = file_path.with_suffix(".test.js")
    else:
        print(f"Skipping: {file_path_str} is not a supported file type for test generation.")
        return

    print(f"Generating tests for {file_path.name}...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        test_code = response.text
        # A common issue is Gemini wrapping code in ```python ... ```
        if test_code.startswith("```"):
            test_code = '\n'.join(test_code.split('\n')[1:-1])

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return

    print(f"Writing test file to: {output_path}")
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(test_code, encoding="utf-8")
    except Exception as e:
        print(f"Error writing test file {output_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_tests.py <file1> <file2> ...")
        sys.exit(1)

    changed_files = sys.argv[1:]
    for file_path in changed_files:
        generate_test_file(file_path)
    print("\nTest generation process completed.")
