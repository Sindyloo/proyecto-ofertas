# 🚀 Guía de Despliegue Gratuito - App de Ofertas

Esta guía te ayudará a desplegar tu aplicación Flask en servidores gratuitos.

## 📋 Opciones de Servidores Gratuitos

### 1. **Render.com** ⭐ (RECOMENDADO - Más Fácil)
- ✅ Plan gratuito disponible
- ✅ Despliegue automático desde GitHub
- ✅ HTTPS incluido
- ✅ Fácil de configurar
- ⚠️ Se "duerme" después de 15 minutos de inactividad (se despierta automáticamente)

**Pasos:**
1. Crea una cuenta en [render.com](https://render.com)
2. Conecta tu repositorio de GitHub
3. Selecciona "New Web Service"
4. Render detectará automáticamente que es Flask
5. Configura:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. ¡Listo! Tu app estará en línea

---

### 2. **Railway.app** ⭐ (Muy Bueno)
- ✅ Plan gratuito con $5 de créditos mensuales
- ✅ Despliegue automático
- ✅ HTTPS incluido
- ✅ No se duerme

**Pasos:**
1. Crea cuenta en [railway.app](https://railway.app)
2. Conecta GitHub
3. Selecciona tu repositorio
4. Railway detectará Flask automáticamente
5. ¡Listo!

---

### 3. **Fly.io** ⭐ (Generoso)
- ✅ Plan gratuito generoso
- ✅ Múltiples regiones
- ✅ HTTPS incluido
- ⚠️ Requiere CLI para configurar

**Pasos:**
1. Instala Fly CLI: `iwr https://fly.io/install.ps1 -useb | iex` (PowerShell)
2. Crea cuenta: `fly auth signup`
3. En tu proyecto: `fly launch`
4. Sigue las instrucciones

---

### 4. **PythonAnywhere**
- ✅ Plan gratuito básico
- ✅ Fácil de usar
- ⚠️ Limitado a 1 app
- ⚠️ URL: `tudominio.pythonanywhere.com`

**Pasos:**
1. Crea cuenta en [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sube tus archivos
3. Configura WSGI
4. ¡Listo!

---

## 🔧 Archivos Necesarios para Despliegue

Ya he creado los siguientes archivos para ti:

- ✅ `Procfile` - Para Render/Railway
- ✅ `runtime.txt` - Versión de Python
- ✅ `gunicorn` agregado a requirements.txt
- ✅ `app.py` modificado para producción

---

## 📝 Pasos Detallados para Render.com

### Paso 1: Preparar el Repositorio

1. **Crea un repositorio en GitHub** (si no lo tienes):
   ```bash
   git init
   git add .
   git commit -m "Preparado para despliegue"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git push -u origin main
   ```

### Paso 2: Desplegar en Render

1. Ve a [render.com](https://render.com) y crea una cuenta
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Selecciona tu repositorio
5. Configura:
   - **Name:** `app-ofertas` (o el nombre que quieras)
   - **Region:** `Oregon (US West)` o el más cercano
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Click en **"Create Web Service"**
7. Espera 5-10 minutos mientras se despliega
8. ¡Tu app estará en línea en una URL como: `https://app-ofertas.onrender.com`!

---

## 📝 Pasos Detallados para Railway.app

### Paso 1: Preparar el Repositorio
(Mismo que Render)

### Paso 2: Desplegar en Railway

1. Ve a [railway.app](https://railway.app) y crea cuenta
2. Click en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Selecciona tu repositorio
5. Railway detectará Flask automáticamente
6. Si no detecta, configura:
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
7. ¡Listo! Tu app estará en línea

---

## ⚙️ Configuración de Variables de Entorno

Si necesitas configurar variables de entorno (por ejemplo, para APIs):

1. En Render: Settings → Environment Variables
2. En Railway: Variables tab
3. Agrega las variables que necesites

---

## 🔍 Verificar que Funciona

Después del despliegue, verifica:

1. Visita la URL de tu app
2. Deberías ver la página de ofertas
3. Prueba el endpoint `/test` para verificar: `https://tu-app.onrender.com/test`

---

## 🐛 Solución de Problemas

### Error: "Module not found"
- Verifica que `requirements.txt` tenga todas las dependencias
- Revisa los logs de despliegue

### Error: "Port already in use"
- No debería pasar, pero si pasa, verifica el `Procfile`

### La app se "duerme" (solo en Render)
- Es normal en el plan gratuito
- Se despierta automáticamente cuando alguien la visita
- La primera carga puede tardar 30-60 segundos

### Error de timeout
- El scraping puede tardar mucho
- Considera aumentar el timeout en la configuración del servicio

---

## 💡 Recomendaciones

1. **Para producción:** Usa `gunicorn` (ya está configurado)
2. **Para desarrollo local:** Sigue usando `python app.py`
3. **Monitoreo:** Revisa los logs regularmente
4. **Backup:** Guarda tus archivos JSON importantes

---

## 📞 ¿Necesitas Ayuda?

- Revisa los logs en el panel de tu servicio
- Verifica que todos los archivos estén en el repositorio
- Asegúrate de que `requirements.txt` esté actualizado

---

## 🎉 ¡Listo!

Tu aplicación estará disponible 24/7 en internet (con las limitaciones del plan gratuito).

**URL de ejemplo:** `https://tu-app.onrender.com`

¡Feliz despliegue! 🚀

