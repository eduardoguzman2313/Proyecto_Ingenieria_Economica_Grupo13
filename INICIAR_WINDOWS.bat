@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo No se encontro .venv en esta carpeta.
    echo Crea el entorno virtual con: python -m venv .venv
    echo Instala las dependencias con: .venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)
echo.
echo Abre esta direccion en Brave cuando inicie FastAPI:
echo http://127.0.0.1:8000
echo.
".venv\Scripts\python.exe" -m uvicorn main:app --reload --port 8000
pause
