@echo off
echo ============================================================
echo 📤 SUBIR PROYECTO A GITHUB
echo ============================================================
echo.
echo Usuario GitHub: Sindyloo
echo Repositorio: proyecto-ofertas
echo URL: https://github.com/Sindyloo/proyecto-ofertas
echo.
echo ============================================================
echo PASO 1: Configurar Git (solo si no está configurado)
echo ============================================================
echo.
set /p GIT_NAME="Ingresa tu nombre completo (ej: Juan Pérez): "
set /p GIT_EMAIL="Ingresa tu email (ej: juan@email.com): "

git config --global user.name "%GIT_NAME%"
git config --global user.email "%GIT_EMAIL%"

echo.
echo ✅ Git configurado correctamente
echo.

echo ============================================================
echo PASO 2: Agregar archivos
echo ============================================================
git add .
echo ✅ Archivos agregados
echo.

echo ============================================================
echo PASO 3: Hacer commit
echo ============================================================
git commit -m "Primera versión: App de ofertas lista para desplegar"
echo ✅ Commit realizado
echo.

echo ============================================================
echo PASO 4: Conectar con GitHub
echo ============================================================
git remote remove origin 2>nul
git remote add origin https://github.com/Sindyloo/proyecto-ofertas.git
echo ✅ Repositorio remoto configurado
echo.

echo ============================================================
echo PASO 5: Subir a GitHub
echo ============================================================
echo.
echo ⚠️  IMPORTANTE:
echo    - Te pedirá tu usuario de GitHub: Sindyloo
echo    - Te pedirá contraseña: Si tienes 2FA, usa un Personal Access Token
echo      (Ver GUIA_GITHUB.md para crear el token)
echo.
pause

git branch -M main
git push -u origin main

echo.
echo ============================================================
if errorlevel 1 (
    echo.
    echo ❌ Hubo un error al subir.
    echo.
    echo Posibles soluciones:
    echo 1. Verifica que el repositorio existe en GitHub
    echo 2. Si tienes 2FA, necesitas un Personal Access Token
    echo    (Lee GUIA_GITHUB.md sección "Si te Pide Autenticación")
    echo 3. Verifica tu usuario y contraseña
) else (
    echo.
    echo ✅ ¡PROYECTO SUBIDO EXITOSAMENTE A GITHUB!
    echo.
    echo 🌐 Tu proyecto está en:
    echo    https://github.com/Sindyloo/proyecto-ofertas
    echo.
    echo 🚀 Ahora puedes desplegarlo en Render, Railway, etc.
    echo    Lee GUIA_DESPLIEGUE.md para más información.
)
echo ============================================================
echo.
pause

