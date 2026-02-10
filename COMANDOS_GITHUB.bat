@echo off
echo ============================================================
echo 📤 SUBIR PROYECTO A GITHUB
echo ============================================================
echo.
echo Este script te ayudará a subir tu proyecto a GitHub.
echo.
echo ⚠️  IMPORTANTE: Antes de ejecutar esto:
echo    1. Debes tener una cuenta en GitHub
echo    2. Debes crear un repositorio en GitHub
echo    3. Debes tener la URL de tu repositorio
echo.
pause

echo.
echo ============================================================
echo PASO 1: Verificar si Git está configurado
echo ============================================================
git config --global user.name >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Git no está configurado. Necesitas configurarlo primero.
    echo.
    set /p GIT_NAME="Ingresa tu nombre: "
    set /p GIT_EMAIL="Ingresa tu email: "
    git config --global user.name "%GIT_NAME%"
    git config --global user.email "%GIT_EMAIL%"
    echo ✅ Git configurado correctamente
) else (
    echo ✅ Git ya está configurado
    git config --global user.name
    git config --global user.email
)

echo.
echo ============================================================
echo PASO 2: Inicializar repositorio Git
echo ============================================================
if exist .git (
    echo ✅ Repositorio Git ya existe
) else (
    git init
    echo ✅ Repositorio Git inicializado
)

echo.
echo ============================================================
echo PASO 3: Agregar archivos
echo ============================================================
git add .
echo ✅ Archivos agregados

echo.
echo ============================================================
echo PASO 4: Hacer commit
echo ============================================================
git commit -m "Primera versión: App de ofertas lista para desplegar"
echo ✅ Commit realizado

echo.
echo ============================================================
echo PASO 5: Conectar con GitHub
echo ============================================================
echo.
echo Ingresa la URL de tu repositorio de GitHub.
echo Ejemplo: https://github.com/tu-usuario/proyecto-ofertas.git
echo.
set /p REPO_URL="URL del repositorio: "

git remote remove origin 2>nul
git remote add origin %REPO_URL%
echo ✅ Repositorio remoto configurado

echo.
echo ============================================================
echo PASO 6: Subir a GitHub
echo ============================================================
echo.
echo ⚠️  Esto te pedirá tu usuario y contraseña de GitHub.
echo    Si tienes autenticación de dos factores, necesitarás
echo    un Personal Access Token en lugar de tu contraseña.
echo.
pause

git branch -M main
git push -u origin main

echo.
echo ============================================================
if errorlevel 1 (
    echo ❌ Hubo un error al subir. Revisa los mensajes arriba.
    echo.
    echo Posibles soluciones:
    echo - Verifica que la URL del repositorio sea correcta
    echo - Usa un Personal Access Token si tienes 2FA activado
    echo - Verifica que tengas permisos en el repositorio
) else (
    echo ✅ ¡PROYECTO SUBIDO EXITOSAMENTE A GITHUB!
    echo.
    echo Ahora puedes desplegar tu app en Render, Railway, etc.
    echo Lee GUIA_DESPLIEGUE.md para más información.
)
echo ============================================================
echo.
pause

