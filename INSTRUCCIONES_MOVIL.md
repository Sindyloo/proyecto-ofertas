# 📱 Instrucciones para Acceder desde tu Celular

## Paso 1: Abrir el Firewall de Windows

**IMPORTANTE:** Ejecuta esto primero para permitir conexiones desde tu celular.

### Opción A: Automático (Recomendado)
1. Abre PowerShell como **Administrador**:
   - Click derecho en el menú Inicio
   - Selecciona "Windows PowerShell (Administrador)" o "Terminal (Administrador)"
2. Navega a la carpeta del proyecto:
   ```powershell
   cd D:\APP-OFERTAS\proyecto_ofertas
   ```
3. Ejecuta el script:
   ```powershell
   .\abrir_firewall.ps1
   ```

### Opción B: Manual
Abre PowerShell como Administrador y ejecuta:
```powershell
New-NetFirewallRule -DisplayName "Flask App" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

## Paso 2: Iniciar el Servidor Flask

En tu terminal normal (no necesita ser administrador):
```bash
python app.py
```

Verás un mensaje como:
```
📱 Acceso desde tu celular:
   http://192.168.0.101:5000
```

## Paso 3: Conectar tu Celular

1. **Asegúrate de que tu celular esté en la misma red WiFi** que tu computadora
2. Abre el navegador en tu celular
3. Ve a la URL que muestra el servidor (ej: `http://192.168.0.101:5000`)
4. Si ves una advertencia de seguridad:
   - Haz clic en **"Continuar al sitio"** o **"Avanzado"** → **"Continuar al sitio (no seguro)"**
   - Es seguro porque estás en tu red local privada

## Solución de Problemas

### ❌ No carga la página
1. Verifica que ambos dispositivos estén en la misma red WiFi
2. Verifica que el servidor Flask esté corriendo
3. Verifica que el firewall esté configurado (Paso 1)
4. Prueba desde tu computadora primero: `http://localhost:5000`

### ❌ Veo "No se puede acceder a este sitio"
1. Verifica la IP en el mensaje del servidor
2. Asegúrate de usar `http://` (no `https://`)
3. Verifica que el puerto sea `:5000`

### ❌ Veo advertencia de seguridad
- Esto es normal con HTTP
- Haz clic en "Continuar al sitio" o "Avanzado" → "Continuar"

## Verificar Conexión

Ejecuta este script para verificar tu configuración:
```bash
python verificar_conexion.py
```

