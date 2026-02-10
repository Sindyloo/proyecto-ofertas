@echo off
echo ============================================================
echo 🚀 INICIANDO SERVIDOR FLASK
echo ============================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.
echo Iniciando servidor Flask...
echo.
echo ⚠️  IMPORTANTE:
echo    - Mantén esta ventana abierta mientras uses el servidor
echo    - Para detener el servidor, presiona Ctrl+C
echo    - Si ves errores, revisa los mensajes en pantalla
echo.
echo ============================================================
echo.

python app.py

pause

