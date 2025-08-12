# 📚 Mi Librería Inteligente

Mi Librería Inteligente es una aplicación web que utiliza la IA multimodal de Google Gemini para analizar y catalogar automáticamente tu colección de libros digitales (PDF y EPUB). Simplemente sube un libro, y la aplicación extraerá su portada, título, autor y le asignará una categoría, guardándolo todo en una base de datos local para que puedas explorar tu biblioteca fácilmente.

## ✨ Características Principales

- **Subida Sencilla:** Arrastra y suelta o selecciona archivos PDF y EPUB para añadir a tu biblioteca.
- **Subida Múltiple:** Sube varios libros a la vez y observa el progreso de cada uno de forma individual.
- **Análisis Inteligente con IA:** Utiliza Google Gemini para extraer metadatos clave (título, autor, categoría) de tus libros, incluso si no están presentes en el archivo, y encuentra la portada.
- **Lectura Integrada:** Lee tus libros (PDF y EPUB) directamente dentro de la aplicación, sin necesidad de software externo. Los PDF se abren en una nueva pestaña para una mejor experiencia.
- **Conversor EPUB a PDF:** Convierte tus archivos EPUB a formato PDF directamente desde la aplicación. El PDF resultante se abre automáticamente en una nueva pestaña.
- **Charla sobre libros con la IA (RAG):** Sube cualquier libro (PDF o EPUB) y mantén una conversación interactiva con la IA sobre su contenido. La IA priorizará la información del libro, pero también puede usar su conocimiento general para responder preguntas más amplias sobre el autor o temas relacionados.
- **Catalogación Automática:** Guarda los libros y sus metadatos en una base de datos local.
- **Biblioteca Visual:** Explora todos tus libros en una vista de galería intuitiva.
- **Filtros por Categoría:** Filtra tu biblioteca por las categorías asignadas por la IA.
- **Buscador Integrado:** Busca libros instantáneamente por título, autor o categoría.
- **Gestión Completa:** Elimina libros individuales o categorías enteras con un solo clic.
- **Acceso Directo:** Abre los archivos originales de tus libros directamente desde la aplicación.
- **Diseño Responsivo:** La interfaz de usuario se adapta automáticamente a diferentes tamaños de pantalla, permitiendo una experiencia fluida tanto en ordenadores de escritorio como en dispositivos móviles (teléfonos y tablets).

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python, FastAPI, SQLAlchemy, Alembic
- **Frontend:** React (JavaScript)
- **IA:** Google Gemini Pro
- **Base de Datos:** SQLite
- **Manejo de Libros:** PyMuPDF (para PDF), EbookLib (para EPUB)

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

### Prerrequisitos

- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js y npm](https://nodejs.org/en/)
- Una clave de API de **Google Gemini**. Puedes obtenerla en [Google AI Studio](https://aistudio.google.com/app/apikey).

### Dependencias Adicionales (Para la Conversión EPUB a PDF)

La herramienta de conversión de EPUB a PDF requiere la instalación de **GTK3**. Si no instalas esta dependencia, el resto de la aplicación funcionará correctamente, pero la herramienta de conversión mostrará un error al intentar convertir.

Sigue las instrucciones para tu sistema operativo:

- **Windows:**
  1. Descarga e instala **MSYS2** desde [su web oficial](https://www.msys2.org/).
  2. Abre la terminal de MSYS2 (no la de Windows) y actualiza el sistema:
     ```bash
     pacman -Syu
     ```
  3. Cierra la terminal y vuelve a abrirla. Actualiza de nuevo:
     ```bash
     pacman -Su
     ```
  4. Instala GTK3:
     ```bash
     pacman -S mingw-w64-x86_64-gtk3
     ```
  5. Añade la carpeta `bin` de MSYS2 a tu **PATH** de Windows. Normalmente se encuentra en `C:\msys64\mingw64\bin`.

- **macOS (usando [Homebrew](https://brew.sh/)):**
  ```bash
  brew install pango
  ```

- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
  ```

### 1. Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

### 2. Configurar el Backend

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

### 3. Configurar las Variables de Entorno

En la raíz del proyecto, crea un archivo llamado `.env` y añade tu clave de API de Gemini. Puedes usar el archivo `.env.example` como plantilla.

**.env**
```
GEMINI_API_KEY="TU_API_KEY_DE_GEMINI_AQUI"
```

### 4. Configurar el Frontend

```bash
# Desde la raíz del proyecto, navega al directorio del frontend
cd frontend

# Instala las dependencias de Node.js
npm install
```

### 5. ¡Ejecutar la Aplicación!

Necesitarás dos terminales abiertas.

- **En la Terminal 1 (para el Backend):**
  ```bash
  # Desde la carpeta 'backend' y con el entorno virtual activado
  uvicorn main:app --reload --port 8001 --host 0.0.0.0
  ```

- **En la Terminal 2 (para el Frontend):**
  ```bash
  # Desde la carpeta 'frontend'
  npm start
  ```

¡Abre tu navegador en `http://localhost:3000` y empieza a construir tu librería inteligente!

**Acceso desde Dispositivos Móviles:**
Para acceder a la aplicación desde un dispositivo móvil en la misma red, asegúrate de que el servidor backend se inicie con `--host 0.0.0.0` (como se muestra arriba). Luego, en tu dispositivo móvil, abre el navegador y navega a `http://<TU_IP_LOCAL>:3000`, donde `<TU_IP_LOCAL>` es la dirección IP de tu ordenador en la red local (por ejemplo, `http://192.168.1.100:3000`).

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
