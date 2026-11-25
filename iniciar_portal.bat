@echo off
chcp 65001 > nul
echo ========================================================
echo        Iniciando Portal da Mulher (Django + SSL)
echo ========================================================

cd /d "%~dp0django_portal_mulher"

set "PYTHON_EXE=.venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
    if exist "C:\Python312\python.exe" (
        set "PYTHON_EXE=C:\Python312\python.exe"
    ) else (
        set "PYTHON_EXE=python"
    )
)

echo Usando Python: %PYTHON_EXE%
echo.

set "DJANGO_DEBUG=True"

start "Django - Portal da Mulher (Porta 8000)" %PYTHON_EXE% manage.py runserver 0.0.0.0:8000
start "SSL Proxy - Portal da Mulher (Porta 443)" %PYTHON_EXE% ssl_proxy.py

echo.
echo Servidores iniciados com sucesso!
echo - HTTP:  http://localhost:8000/
echo - HTTPS: https://localhost/
echo ========================================================
pause
