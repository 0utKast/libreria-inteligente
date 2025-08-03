@echo off
setlocal enabledelayedexpansion
echo ========================================
echo    Deteniendo Servidores de la Libreria
echo ========================================

echo.
echo Buscando y deteniendo el servidor del Frontend (en puerto 3000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000" ^| findstr "LISTENING"') do (
    echo Cerrando proceso con PID %%a y sus subprocesos...
    taskkill /F /PID %%a /T
)

echo.
echo Buscando y deteniendo el servidor del Backend (en puerto 8001)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8001" ^| findstr "LISTENING"') do (
    set "backend_pid=%%a"
    if defined backend_pid (
        echo Cerrando proceso del backend con PID !backend_pid! y sus subprocesos...
        taskkill /F /PID !backend_pid! /T

        REM Encontrar el PID del proceso padre (la ventana de cmd que lo lanzó)
        for /f "tokens=2" %%x in ('wmic process where "ProcessId=!backend_pid!" get ParentProcessId ^| findstr /v "ParentProcessId"') do (
            set "parent_pid=%%x"
            if defined parent_pid (
                echo Cerrando proceso padre con PID !parent_pid!...
                taskkill /F /PID !parent_pid! /T
            )
        )
    )
)

echo.
echo Todos los procesos han sido detenidos.
pause