# Guía de Instalación

Sigue estos pasos para configurar y ejecutar "Mi Librería Inteligente" en tu máquina local.

## Prerrequisitos

Asegúrate de tener instalado lo siguiente:

*   **Python 3.9+:** Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
*   **Node.js y npm:** Descárgalos desde [nodejs.org](https://nodejs.org/en/).
*   Una clave de API de **Google Gemini:** Obtén una en [Google AI Studio](https://aistudio.google.com/app/apikey).

### Dependencias Adicionales (Para la Conversión EPUB a PDF)

La herramienta de conversión de EPUB a PDF requiere la instalación de **GTK3**. Si no instalas esta dependencia, el resto de la aplicación funcionará correctamente, pero la herramienta de conversión mostrará un error al intentar convertir.

Sigue las instrucciones para tu sistema operativo:

*   **Windows:**
    1.  Descarga e instala **MSYS2** desde [su web oficial](https://www.msys2.org/).
    2.  Abre la terminal de MSYS2 (no la de Windows) y actualiza el sistema:
        ```bash
        pacman -Syu
        ```
    3.  Cierra la terminal y vuelve a abrirla. Actualiza de nuevo:
        ```bash
        pacman -Su
        ```
    4.  Instala GTK3:
        ```bash
        pacman -S mingw-w64-x86_64-gtk3
        ```
    5.  Añade la carpeta `bin` de MSYS2 a tu **PATH** de Windows. Normalmente se encuentra en `C:\msys64\mingw64\bin`.

*   **macOS (usando [Homebrew](https://brew.sh/)):**
    ```bash
    brew install pango
    ```

*   **Linux (Debian/Ubuntu):**
    ```bash
    sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
    ```

## 1. Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

## 2. Configurar el Backend

```bash
# Navega al directorio del backend
cd backend

# Crea y activa un entorno virtual
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En macOS/Linux:
# source .venv/bin/activate

# Instala las dependencias de Python
pip install -r requirements.txt

# Crea la base de datos inicial
alembic upgrade head
```

## 3. Configurar las Variables de Entorno

En la raíz del proyecto, crea un archivo llamado `.env` y añade tu clave de API de Gemini. Puedes usar el archivo `.env.example` como plantilla.

**`.env`**
```
GEMINI_API_KEY="TU_API_KEY_DE_GEMINI_AQUI"
```

## 4. Configurar el Frontend

```bash
# Desde la raíz del proyecto, navega al directorio del frontend
cd frontend

# Instala las dependencias de Node.js
npm install
```

## 5. ¡Ejecutar la Aplicación!

Necesitarás dos terminales abiertas.

*   **En la Terminal 1 (para el Backend):**
    ```bash
    # Desde la carpeta 'backend' y con el entorno virtual activado
    uvicorn main:app --reload --port 8001
    ```

*   **En la Terminal 2 (para el Frontend):**
    ```bash
    # Desde la carpeta 'frontend'
    npm start
    ```

¡Abre tu navegador en `http://localhost:3000` y empieza a construir tu librería inteligente!
