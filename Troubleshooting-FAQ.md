# Resolución de Problemas y Preguntas Frecuentes

Esta sección te ayudará a solucionar problemas comunes y responderá a preguntas frecuentes sobre "Mi Librería Inteligente".

## Problemas Comunes de Instalación

### `ModuleNotFoundError: No module named '...'`

Este error indica que una de las dependencias de Python no está instalada correctamente en tu entorno virtual.

**Solución:**
1.  Asegúrate de que tu entorno virtual esté activado:
    *   **Windows:** `cd backend` y luego `.venv\Scripts\activate`
    *   **macOS/Linux:** `cd backend` y luego `source .venv/bin/activate`
2.  Instala la dependencia que falta. Por ejemplo, si el error es `No module named 'chromadb'`, ejecuta:
    ```bash
    pip install chromadb
    ```
    Repite este paso para cualquier otra dependencia que falte (`PyPDF2`, `tiktoken`, `ebooklib`, etc.).

### Problemas con GTK3 para la Conversión EPUB a PDF

Si la herramienta de conversión de EPUB a PDF no funciona y ves errores relacionados con GTK3, asegúrate de haber seguido las instrucciones de instalación de GTK3 para tu sistema operativo en la [Guía de Instalación](Installation-Guide).

## Problemas con los Servidores

### El Backend no se inicia (Puerto 8001)

*   **Puerto en Uso:** Otro proceso podría estar utilizando el puerto 8001. Puedes intentar cambiar el puerto en el comando `uvicorn` en `start.bat` o liberar el puerto.
*   **Errores en el Código:** Revisa la salida de la terminal del backend para ver si hay errores de Python que impidan que el servidor se inicie.

### El Frontend no se inicia (Puerto 3000)

*   **Puerto en Uso:** Otro proceso podría estar utilizando el puerto 3000. Puedes intentar cambiar el puerto en `package.json` o liberar el puerto.
*   **Errores de Compilación:** Revisa la salida de la terminal del frontend para ver si hay errores de JavaScript que impidan que la aplicación se compile.

### `stop.bat` no detiene el servidor Backend

Este problema suele estar relacionado con cómo el script identifica y termina el proceso. Asegúrate de que tu `stop.bat` esté actualizado con la última versión que incluye la detección del proceso padre y el uso de `setlocal enabledelayedexpansion`.

## Problemas con la IA (Gemini)

### `404 models/gemini-pro is not found...`

Este error indica que el modelo de Gemini especificado no está disponible o no es compatible con la operación en tu región o con tu clave de API.

**Solución:** Asegúrate de que el modelo configurado en `backend/rag.py` (actualmente `gemini-1.5-flash`) sea compatible con tu cuenta de Gemini. Puedes consultar la documentación de Google AI Studio para ver los modelos disponibles.

### Respuestas de la IA en Inglés o Demasiado Restrictivas

Si la IA no responde en español o es demasiado estricta y dice "No puedo responder a esta pregunta..." incluso para preguntas generales:

**Solución:** Revisa el `prompt` configurado en `backend/rag.py`. Asegúrate de que incluya las instrucciones para responder en español y para usar el conocimiento general cuando el contexto del libro no sea suficiente.

### Errores al Procesar Libros para RAG (`NoneType` o `dict` no puede ser `await`ed)

Estos errores indican un problema con la forma en que las funciones asíncronas y síncronas interactúan con la API de Gemini.

**Solución:** Asegúrate de que las funciones `get_embedding`, `process_book_for_rag` y `query_rag` en `backend/rag.py` estén correctamente definidas como `async` o síncronas según corresponda, y que los `await` se utilicen solo con funciones asíncronas.

## Preguntas Frecuentes (FAQ)

**P: ¿Puedo usar cualquier tipo de archivo de libro?**
**R:** Actualmente, la aplicación soporta archivos PDF y EPUB.

**P: ¿Necesito una conexión a Internet para usar la aplicación?**
**R:** Sí, necesitas una conexión a Internet para que la aplicación pueda comunicarse con la API de Google Gemini para el análisis de libros y la función de chat RAG.

**P: ¿Mis libros se suben a algún servidor externo?**
**R:** No, tus libros se procesan localmente en tu máquina. Solo los fragmentos de texto relevantes y tus preguntas se envían a la API de Gemini para su análisis y respuesta, no el contenido completo del libro.
