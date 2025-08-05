@echo off
echo ========================================
echo   Iniciando Servidores de la Libreria
echo ========================================

REM Iniciar el servidor del Backend en una nueva ventana
echo Iniciando Backend en http://localhost:8001 ...
START "Backend" cmd /c "cd backend && C:\proyectos_python\libreria\backend\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8001 --host 0.0.0.0"

REM Iniciar el servidor del Frontend en una nueva ventana
echo Iniciando Frontend en http://localhost:3000 ...
START "Frontend" cmd /c "cd frontend && npm start"

echo.
echo Servidores iniciados en segundo plano.
echo Puedes cerrar esta ventana.
timeout /t 5 >nul
