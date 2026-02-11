# 🚀 Guía Paso a Paso: Desplegar en Render.com

Ya que tu proyecto está en GitHub, aquí está la explicación detallada para desplegarlo en Render.com.

---

## 📋 INFORMACIÓN DE TU PROYECTO

- **Usuario GitHub:** Sindyloo
- **Repositorio:** proyecto-ofertas
- **URL del repositorio:** https://github.com/Sindyloo/proyecto-ofertas

---

## 🎯 PASO 1: Crear Cuenta en Render.com

1. Ve a **https://render.com**
2. Click en el botón **"Get Started for Free"** o **"Sign Up"**
3. Tienes 2 opciones para registrarte:
   - **Opción A:** Con GitHub (RECOMENDADO - más fácil)
     - Click en **"Sign up with GitHub"**
     - Te pedirá autorizar a Render para acceder a tus repositorios
     - Acepta y listo
   - **Opción B:** Con email
     - Ingresa tu email y crea una contraseña
     - Verifica tu email

---

## 🎯 PASO 2: Crear un Nuevo Web Service

1. Una vez dentro de Render, verás un panel (dashboard)
2. En la parte superior, busca el botón **"New +"** (arriba a la izquierda)
3. Click en **"New +"** → Se abrirá un menú
4. Selecciona **"Web Service"** (el primero de la lista)

---

## 🎯 PASO 3: Conectar tu Repositorio de GitHub

1. Render te mostrará una pantalla para conectar un repositorio
2. Si te registraste con GitHub, verás una lista de tus repositorios
3. **Busca y selecciona:** `Sindyloo/proyecto-ofertas`
4. Si no aparece, click en **"Configure account"** o **"Connect GitHub"**
5. Autoriza a Render para acceder a tus repositorios
6. Una vez conectado, selecciona **`proyecto-ofertas`**

---

## 🎯 PASO 4: Configurar el Servicio

Render te mostrará un formulario con varias opciones. Aquí está qué poner en cada campo:

### 📝 Campos a Configurar:

1. **Name** (Nombre del servicio):
   - Escribe: `app-ofertas` o `proyecto-ofertas`
   - Este será parte de tu URL: `https://app-ofertas.onrender.com`

2. **Region** (Región):
   - Selecciona la más cercana a ti:
     - `Oregon (US West)` - Para América
     - `Frankfurt (EU Central)` - Para Europa
     - `Singapore (AP Southeast)` - Para Asia
   - Si no estás seguro, usa `Oregon (US West)`

3. **Branch** (Rama):
   - Debe decir: `main`
   - Si dice otra cosa, cámbialo a `main`

4. **Root Directory** (Directorio raíz):
   - **Déjalo vacío** (a menos que tu app esté en una subcarpeta)

5. **Runtime** (Entorno de ejecución):
   - Debe decir: `Python 3`
   - Si no, selecciónalo del menú

6. **Build Command** (Comando de construcción):
   - Escribe exactamente: `pip install -r requirements.txt`
   - Esto instalará todas las dependencias de tu proyecto

7. **Start Command** (Comando de inicio):
   - Escribe exactamente: `gunicorn app:app`
   - Esto iniciará tu aplicación Flask usando Gunicorn (servidor de producción)

### ⚙️ Configuraciones Avanzadas (Opcional):

- **Instance Type:** Déjalo en `Free` (plan gratuito)
- **Auto-Deploy:** Déjalo en `Yes` (se actualizará automáticamente cuando hagas cambios)

---

## 🎯 PASO 5: Crear el Servicio

1. Revisa que todos los campos estén correctos
2. Scroll hacia abajo y busca el botón **"Create Web Service"**
3. Click en **"Create Web Service"**

---

## 🎯 PASO 6: Esperar el Despliegue

1. Render comenzará a desplegar tu aplicación
2. Verás una pantalla con el progreso:
   - **"Building"** - Instalando dependencias
   - **"Deploying"** - Desplegando la aplicación
   - **"Live"** - ¡Tu app está en línea!

3. **Tiempo estimado:** 5-10 minutos (la primera vez puede tardar más)

4. Puedes ver los logs en tiempo real haciendo click en **"Logs"**

---

## 🎯 PASO 7: ¡Tu App Está en Línea!

1. Cuando veas el estado **"Live"** (verde), tu app está funcionando
2. Verás una URL como: `https://app-ofertas.onrender.com`
3. **Click en la URL** o cópiala y ábrela en tu navegador
4. ¡Deberías ver tu aplicación funcionando!

---

## ✅ VERIFICAR QUE FUNCIONA

1. **Página principal:**
   - Ve a: `https://app-ofertas.onrender.com`
   - Deberías ver la página de ofertas

2. **Endpoint de prueba:**
   - Ve a: `https://app-ofertas.onrender.com/test`
   - Deberías ver un JSON con: `{"status": "ok", ...}`

---

## 📸 RESUMEN VISUAL DE LA INTERFAZ

```
Render Dashboard
├── [New +] ← Click aquí
│   ├── Web Service ← Selecciona esto
│   ├── Background Worker
│   └── ...
│
Formulario de Configuración:
├── Connect Repository: [Sindyloo/proyecto-ofertas] ← Selecciona tu repo
├── Name: [app-ofertas]
├── Region: [Oregon (US West)]
├── Branch: [main]
├── Runtime: [Python 3]
├── Build Command: [pip install -r requirements.txt]
├── Start Command: [gunicorn app:app --config gunicorn.conf.py]
└── [Create Web Service] ← Click aquí
```

---

## ⚠️ IMPORTANTE: Plan Gratuito

### La App se "Duerme"
- En el plan gratuito, tu app se "duerme" después de **15 minutos de inactividad**
- Esto es normal y no es un error
- Cuando alguien visite tu app, se "despertará" automáticamente
- La primera carga después de dormir puede tardar **30-60 segundos**

### Límites del Plan Gratuito
- ✅ HTTPS incluido
- ✅ Dominio personalizado (opcional)
- ✅ Despliegue automático desde GitHub
- ⚠️ Se duerme después de 15 min de inactividad
- ⚠️ 750 horas gratis por mes (suficiente para uso personal)

---

## 🔄 ACTUALIZAR TU APP

Cada vez que hagas cambios en GitHub:

1. Haz commit y push a GitHub:
   ```bash
   git add .
   git commit -m "Descripción de cambios"
   git push
   ```

2. Render detectará automáticamente los cambios (si tienes Auto-Deploy activado)

3. Irá a la sección **"Events"** en Render y verás un nuevo despliegue

4. Espera 2-5 minutos y tu app estará actualizada

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "Build failed"
**Causa:** Faltan dependencias o error en requirements.txt
**Solución:**
1. Ve a la pestaña **"Logs"** en Render
2. Lee el error específico
3. Verifica que `requirements.txt` tenga todas las dependencias
4. Asegúrate de que `gunicorn` esté en requirements.txt

### ❌ Error: "Module not found"
**Causa:** Falta una dependencia
**Solución:**
1. Agrega la dependencia faltante a `requirements.txt`
2. Haz commit y push a GitHub
3. Render se actualizará automáticamente

### ❌ La app no carga / Timeout
**Causa:** El scraping puede tardar mucho tiempo
**Solución:**
1. El proyecto ahora incluye `gunicorn.conf.py` con timeout de 300 segundos configurado automáticamente
2. Si aún tienes problemas, ve a **Settings** → **Advanced** en Render
3. Aumenta el **"Health Check Timeout"** a 300 segundos
4. Guarda los cambios

### ❌ Error: "Port already in use"
**Causa:** Configuración incorrecta
**Solución:**
- Verifica que el **Start Command** sea exactamente: `gunicorn app:app`
- No uses `python app.py` en producción

### ⏰ La app tarda mucho en cargar
**Causa:** La app estaba "dormida"
**Solución:**
- Es normal en el plan gratuito
- Espera 30-60 segundos la primera vez
- Las siguientes cargas serán más rápidas

---

## 📊 VER LOGS Y MONITOREAR

1. En el dashboard de Render, click en tu servicio
2. Ve a la pestaña **"Logs"**
3. Verás todos los mensajes de tu aplicación en tiempo real
4. Útil para debuggear problemas

---

## 🎉 ¡LISTO!

Tu aplicación estará disponible en:
**https://app-ofertas.onrender.com** (o el nombre que elegiste)

Puedes compartir esta URL con quien quieras y tu app estará accesible desde cualquier lugar del mundo.

---

## 💡 TIPS ADICIONALES

1. **Dominio personalizado:** Puedes agregar tu propio dominio en Settings → Custom Domain
2. **Variables de entorno:** Si necesitas configurar variables, ve a Settings → Environment
3. **Backups:** Render hace backups automáticos, pero también guarda tus archivos JSON importantes
4. **Monitoreo:** Revisa los logs regularmente para ver cómo funciona tu app

---

¿Tienes alguna duda? ¡Pregunta!

