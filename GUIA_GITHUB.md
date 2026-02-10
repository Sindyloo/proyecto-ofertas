# 📤 Guía: Subir tu Proyecto a GitHub

Esta guía te ayudará a subir tu proyecto a GitHub paso a paso.

## 📋 Paso 1: Crear una Cuenta en GitHub

Si aún no tienes cuenta:

1. Ve a [github.com](https://github.com)
2. Click en **"Sign up"**
3. Completa el formulario
4. Verifica tu email

---

## 📋 Paso 2: Crear un Repositorio en GitHub

1. Una vez dentro de GitHub, click en el **"+"** (arriba a la derecha)
2. Selecciona **"New repository"**
3. Completa:
   - **Repository name:** `proyecto-ofertas` (o el nombre que quieras)
   - **Description:** "App de ofertas de Adidas y otras tiendas"
   - **Visibility:** Elige **Public** (gratis) o **Private** (si quieres que sea privado)
   - ⚠️ **NO marques** "Add a README file" (ya tenemos archivos)
   - ⚠️ **NO marques** "Add .gitignore" (ya lo creamos)
   - ⚠️ **NO marques** "Choose a license"
4. Click en **"Create repository"**

---

## 📋 Paso 3: Configurar Git (Solo la Primera Vez)

Abre PowerShell o Terminal en la carpeta de tu proyecto y ejecuta:

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

**Ejemplo:**
```powershell
git config --global user.name "Juan Pérez"
git config --global user.email "juan@email.com"
```

---

## 📋 Paso 4: Inicializar Git en tu Proyecto

En PowerShell, dentro de tu carpeta del proyecto (`D:\APP-OFERTAS\proyecto_ofertas`):

```powershell
git init
```

---

## 📋 Paso 5: Agregar todos los Archivos

```powershell
git add .
```

Esto agregará todos los archivos al repositorio (excepto los que están en `.gitignore`).

---

## 📋 Paso 6: Hacer el Primer Commit

```powershell
git commit -m "Primera versión: App de ofertas lista para desplegar"
```

---

## 📋 Paso 7: Conectar con GitHub

GitHub te mostrará una URL como esta después de crear el repositorio:

```
https://github.com/TU_USUARIO/proyecto-ofertas.git
```

Ejecuta (reemplaza con TU URL):

```powershell
git remote add origin https://github.com/TU_USUARIO/proyecto-ofertas.git
```

**Ejemplo:**
```powershell
git remote add origin https://github.com/juanperez/proyecto-ofertas.git
```

---

## 📋 Paso 8: Subir el Código a GitHub

```powershell
git branch -M main
git push -u origin main
```

Te pedirá tu usuario y contraseña de GitHub. Si tienes autenticación de dos factores, necesitarás un **Personal Access Token** (ver abajo).

---

## 🔐 Si te Pide Autenticación

GitHub ya no acepta contraseñas normales. Necesitas un **Personal Access Token**:

### Crear un Personal Access Token:

1. Ve a GitHub → Click en tu foto (arriba derecha) → **Settings**
2. En el menú izquierdo, click en **Developer settings**
3. Click en **Personal access tokens** → **Tokens (classic)**
4. Click en **Generate new token** → **Generate new token (classic)**
5. Completa:
   - **Note:** "Token para proyecto-ofertas"
   - **Expiration:** Elige cuánto tiempo quieres (90 días, 1 año, etc.)
   - **Select scopes:** Marca **repo** (esto da acceso completo a repositorios)
6. Click en **Generate token**
7. **⚠️ COPIA EL TOKEN INMEDIATAMENTE** (solo se muestra una vez)
8. Cuando `git push` te pida la contraseña, **pega el token** en lugar de tu contraseña

---

## ✅ Verificar que Funcionó

1. Ve a tu repositorio en GitHub: `https://github.com/TU_USUARIO/proyecto-ofertas`
2. Deberías ver todos tus archivos ahí

---

## 🔄 Para Actualizar el Código en el Futuro

Cada vez que hagas cambios y quieras subirlos:

```powershell
git add .
git commit -m "Descripción de los cambios"
git push
```

---

## 🐛 Solución de Problemas

### Error: "fatal: not a git repository"
- Ejecuta `git init` primero

### Error: "Please tell me who you are"
- Ejecuta los comandos de configuración del Paso 3

### Error: "remote origin already exists"
- Ejecuta: `git remote remove origin`
- Luego vuelve a ejecutar el Paso 7

### Error: "Authentication failed"
- Usa un Personal Access Token en lugar de tu contraseña

### Error: "Permission denied"
- Verifica que la URL del repositorio sea correcta
- Verifica que tengas permisos en el repositorio

---

## 📝 Comandos Rápidos (Resumen)

```powershell
# 1. Inicializar
git init

# 2. Configurar (solo primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"

# 3. Agregar archivos
git add .

# 4. Hacer commit
git commit -m "Primera versión"

# 5. Conectar con GitHub
git remote add origin https://github.com/TU_USUARIO/proyecto-ofertas.git

# 6. Subir
git branch -M main
git push -u origin main
```

---

## 🎉 ¡Listo!

Una vez que tu código esté en GitHub, podrás desplegarlo en Render, Railway u otros servicios siguiendo la guía de despliegue.

---

## 💡 Tip: Usar GitHub Desktop (Alternativa Más Fácil)

Si prefieres una interfaz gráfica en lugar de comandos:

1. Descarga [GitHub Desktop](https://desktop.github.com/)
2. Instálalo
3. Inicia sesión con tu cuenta de GitHub
4. Click en **File** → **Add Local Repository**
5. Selecciona tu carpeta del proyecto
6. Click en **Publish repository**
7. ¡Listo!

---

¿Necesitas ayuda con algún paso? ¡Pregunta!

