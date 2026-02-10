@echo off
echo ============================================================
echo 🔥 ABRIENDO FIREWALL PARA FLASK
echo ============================================================
echo.
echo Este script debe ejecutarse como Administrador
echo.
pause

REM Abrir puerto 5000 en el firewall usando netsh
netsh advfirewall firewall add rule name="Flask App" dir=in action=allow protocol=TCP localport=5000

if %errorlevel% == 0 (
    echo.
    echo ✅ Regla del firewall creada exitosamente
    echo.
    echo 🚀 Ahora puedes iniciar el servidor Flask:
    echo    python app.py
    echo.
    echo 📱 Y acceder desde tu celular usando la IP que muestra
) else (
    echo.
    echo ❌ Error creando regla del firewall
    echo.
    echo 💡 Asegúrate de ejecutar este script como Administrador:
    echo    Click derecho en el archivo → Ejecutar como administrador
)

echo.
pause


