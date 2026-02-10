from flask import Flask, render_template, Response
from scraper import obtener_ofertas_por_categoria, CATEGORIAS
import sys
import json
import os
from datetime import datetime

app = Flask(__name__)
HISTORIAL_FILE = "historial_ofertas.json"

def cargar_historial():
    """Carga el historial anterior de ofertas"""
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def guardar_historial(datos):
    """Guarda el historial actual de ofertas"""
    try:
        with open(HISTORIAL_FILE, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando historial: {e}", file=sys.stderr, flush=True)

def comparar_productos(productos_actuales, productos_anteriores_dict):
    """Compara productos actuales con anteriores y marca cambios"""
    productos_anteriores_dict = productos_anteriores_dict or {}
    
    for producto in productos_actuales:
        url = producto.get('url', '')
        if not url:
            continue
            
        producto_anterior = productos_anteriores_dict.get(url)
        
        if producto_anterior:
            # Producto existente - comparar precios
            desc_actual = producto.get('descuento_num', 0)
            desc_anterior = producto_anterior.get('descuento_num', 0)
            precio_actual = producto.get('precio', '')
            
            # Extraer precio numérico para comparación
            try:
                if precio_actual.startswith('S/ '):
                    precio_num_actual = float(precio_actual.replace('S/ ', '').replace(',', ''))
                    precio_num_anterior_str = producto_anterior.get('precio', '0').replace('S/ ', '').replace(',', '')
                    precio_num_anterior = float(precio_num_anterior_str) if precio_num_anterior_str else 0
                    
                    # Si el precio bajó O el descuento aumentó, es mejor
                    if precio_num_actual < precio_num_anterior or desc_actual > desc_anterior:
                        producto['bajo_precio'] = True
                        producto['precio_anterior'] = producto_anterior.get('precio', '')
                        producto['descuento_anterior'] = producto_anterior.get('descuento', '')
            except:
                pass
        else:
            # Producto nuevo - marcar como nuevo
            producto['producto_nuevo'] = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test")
def test():
    """Endpoint de prueba para verificar que el servidor funciona"""
    return {
        "status": "ok",
        "message": "Servidor Flask funcionando correctamente",
        "timestamp": datetime.now().isoformat()
    }

@app.route("/api/ofertas/stream")
def ofertas_stream():
    """Endpoint que devuelve ofertas por categoría usando Server-Sent Events"""
    # Cargar historial anterior
    historial = cargar_historial()
    
    # Convertir lista anterior a diccionario por URL para búsqueda rápida
    productos_anteriores_dict = {}
    for categoria_data in historial.get('categorias', []):
        for producto in categoria_data.get('productos', []):
            url = producto.get('url', '')
            if url:
                productos_anteriores_dict[url] = producto
    
    def generate():
        try:
            yield f"data: {json.dumps({'type': 'start', 'total': len(CATEGORIAS)})}\n\n"
            
            todas_las_categorias_resultado = []
            
            for i, categoria in enumerate(CATEGORIAS, 1):
                try:
                    yield f"data: {json.dumps({'type': 'categoria_iniciando', 'categoria': categoria['name'], 'numero': i, 'total': len(CATEGORIAS)})}\n\n"
                    
                    resultado = obtener_ofertas_por_categoria(categoria)
                    
                    # Comparar productos con historial
                    comparar_productos(resultado['productos'], productos_anteriores_dict)
                    
                    todas_las_categorias_resultado.append(resultado)
                    
                    yield f"data: {json.dumps({'type': 'categoria_completa', 'categoria': resultado['categoria'], 'productos': resultado['productos'], 'numero': i, 'total': len(CATEGORIAS)})}\n\n"
                except Exception as e:
                    print(f"Error procesando categoría {categoria.get('name', 'desconocida')}: {e}", file=sys.stderr, flush=True)
                    import traceback
                    traceback.print_exc(file=sys.stderr)
                    # Continuar con la siguiente categoría
                    todas_las_categorias_resultado.append({
                        'categoria': categoria.get('name', 'Desconocida'),
                        'productos': []
                    })
                    yield f"data: {json.dumps({'type': 'categoria_completa', 'categoria': categoria.get('name', 'Desconocida'), 'productos': [], 'numero': i, 'total': len(CATEGORIAS), 'error': str(e)})}\n\n"
            
            # Guardar historial después de procesar todas las categorías
            # Crear nuevo diccionario con productos actuales
            productos_actuales_dict = {}
            for categoria_data in todas_las_categorias_resultado:
                for producto in categoria_data.get('productos', []):
                    url = producto.get('url', '')
                    if url:
                        productos_actuales_dict[url] = producto
            
            historial_nuevo = {
                'fecha': datetime.now().isoformat(),
                'categorias': todas_las_categorias_resultado,
                'productos': productos_actuales_dict  # Guardamos el dict para comparación rápida
            }
            guardar_historial(historial_nuevo)
            
            yield f"data: {json.dumps({'type': 'fin'})}\n\n"
        except Exception as e:
            print(f"Error crítico en generate(): {e}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc(file=sys.stderr)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    import socket
    import os
    
    # Obtener el puerto desde variable de entorno (para producción) o usar 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    # En producción, debug debe estar desactivado
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Obtener la IP local de manera más confiable
    def get_local_ip():
        try:
            # Conectar a un servidor externo para obtener la IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            try:
                hostname = socket.gethostname()
                return socket.gethostbyname(hostname)
            except:
                return "127.0.0.1"
    
    local_ip = get_local_ip()
    
    print("\n" + "="*50)
    print("🚀 Servidor Flask iniciado")
    print("="*50)
    print(f"📱 Acceso desde tu celular:")
    print(f"   http://{local_ip}:{port}")
    print(f"")
    print(f"💻 Acceso local:")
    print(f"   http://localhost:{port}")
    print(f"   http://127.0.0.1:{port}")
    print("")
    print("⚠️  IMPORTANTE:")
    print("   1. Asegúrate de que tu celular esté en la misma red WiFi")
    print("   2. Si ves advertencia de seguridad, haz clic en 'Continuar al sitio'")
    print("   3. Si no carga, verifica el firewall de Windows")
    print("="*50 + "\n")
    
    # Usar HTTP simple (sin SSL) para evitar problemas
    try:
        app.run(host='0.0.0.0', port=port, debug=debug_mode, threaded=True, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e) or "address is already in use" in str(e).lower():
            print("\n❌ ERROR: El puerto {} ya está en uso".format(port))
            print("   Cierra otros programas que usen el puerto {}".format(port))
            print("   O cambia el puerto en app.py")
        else:
            print(f"\n❌ ERROR al iniciar servidor: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
