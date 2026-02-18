import requests
import sys
import json
import re
import time
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

API_URL = "https://www.falabella.com.pe/s/browse/v1/listing/pe"
ADIDAS_API_BASE = "https://www.adidas.pe"

# Definir todas las categorías a consultar
CATEGORIAS = [
    {"id": "cat7720500", "name": "Ropa-interior-y-pijamas"},
    {"id": "cat560663", "name": "Maquillaje"},
    {"id": "cat4100462", "name": "⭐ MANGO MUJER > 50%", "marca_especial": "MANGO", "descuento_minimo": 50, "categoria_base": "Moda-Mujer"},
    {"id": "CATG11988", "name": "Baño", "vendedores": "FALABELLA::SODIMAC::TOTTUS"},
    {"id": "cat40571", "name": "Deportes-y-aire-libre"},
    {"id": "cat1470548", "name": "Zapatillas"},
    {"id": "cat1470530", "name": "Sandalias"},
    {"id": "CATG36068", "name": "Menaje", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "CATG11951", "name": "Muebles-y-Organizacion", "vendedores": "FALABELLA::SODIMAC"},
    {"id": "cat11140487", "name": "Dermocosmetica"},
    {"id": "cat4220604", "name": "Carteras-y-bolsos"},
    {"id": "adidas_mujer_60", "name": "🔥 ADIDAS MUJER > 40%", "tipo": "adidas", "url": "/mujer?grid=true&sale_percentage_es_pe=50%7C55%7C60%7C70&sort=price-low-to-high", "descuento_minimo": 30},
    {"id": "cat13920465", "name": "Utiles-de-aseo-y-limpieza", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "cat11380472", "name": "Navidad"},
    {"id": "cat4100462", "name": "Moda-Mujer"},
    {"id": "G16130113", "name": "Belleza"},
    {"id": "CATG12022", "name": "Moda-Hombre"},
    {"id": "cat40497", "name": "Mundo-Bebe", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "CATG35344", "name": "Ninos-y-Juguetes"},
    {"id": "cat6370551", "name": "Televisores-Smart-TV", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "cat800582", "name": "Audifonos", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "cat1830468", "name": "Smartwatch-y-wearables", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "cat40567", "name": "Tecnologia-para-la-Belleza", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "cat270476", "name": "Tablets", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "cat6370558", "name": "Electrodomesticos-de-Cocina", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "cat40712", "name": "Laptops", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "cat760706", "name": "Celulares-y-Telefonos", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "cat6370521", "name": "Linea-blanca", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "CATG11951", "name": "Muebles-y-Organizacion", "vendedores": "FALABELLA::SODIMAC"},
    {"id": "CATG11989", "name": "Cocina", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "CATG11946", "name": "Construccion", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "CATG36090", "name": "Calzado-y-zapatillas"},
    {"id": "cat1470526", "name": "Zapatos"},
    {"id": "cat50684", "name": "Dormitorio", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "CATG46233", "name": "Pinturas", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "cat8050466", "name": "Mascotas", "vendedores": "FALABELLA::TOTTUS::SODIMAC"},
    {"id": "cat40727", "name": "Perfumes"}

]

# ============================================================================
# FUNCIONES PARA ADIDAS (INDEPENDIENTES)
# ============================================================================

def obtener_productos_adidas(url_path, descuento_minimo=60, max_pages=None):
    """Obtiene productos de Adidas usando la API JSON de Next.js directamente"""
    all_products = []
    
    # Crear una sesión para mantener cookies
    session = requests.Session()
    
    # Headers para la API JSON de Next.js
    session.headers.update({
        "Accept": "application/json",
        "Accept-Language": "es-PE,es;q=0.9,en-US;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://www.adidas.pe/",
    })
    
    MAX_PAGES_SAFETY = 20
    start_index = 0
    view_size = 48
    page = 1
    
    # Extraer el path de la URL (ej: "mujer" de "/mujer?grid=true&...")
    parsed = urlparse(url_path)
    path_name = parsed.path.strip('/') or 'mujer'  # Default a 'mujer' si no hay path
    
    # Construir URL completa de la página
    page_url = f"{ADIDAS_API_BASE}/{path_name}"
    if parsed.query:
        page_url += f"?{parsed.query}"
    
    print(f"DEBUG: [ADIDAS] Iniciando obtención de productos desde: {url_path}", file=sys.stderr, flush=True)
    
    # Intentar obtener buildId desde el HTML de la página
    build_id = None
    try:
        print(f"DEBUG: [ADIDAS] Intentando obtener buildId desde HTML...", file=sys.stderr, flush=True)
        html_response = session.get(page_url, timeout=30)
        if html_response.status_code == 200:
            # Buscar buildId en el HTML
            build_match = re.search(r'/_next/data/([a-zA-Z0-9_-]+)/', html_response.text)
            if build_match:
                build_id = build_match.group(1)
                print(f"DEBUG: [ADIDAS] BuildId encontrado: {build_id}", file=sys.stderr, flush=True)
            else:
                # Intentar buscar en __NEXT_DATA__
                next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_response.text, re.DOTALL)
                if next_data_match:
                    try:
                        next_data = json.loads(next_data_match.group(1))
                        build_id = next_data.get("buildId")
                        if build_id:
                            print(f"DEBUG: [ADIDAS] BuildId obtenido desde __NEXT_DATA__: {build_id}", file=sys.stderr, flush=True)
                    except:
                        pass
    except Exception as e:
        print(f"DEBUG: [ADIDAS] Error obteniendo buildId: {e}, continuando sin él", file=sys.stderr, flush=True)
    
    # Si no se obtuvo buildId, usar algunos valores comunes conocidos de Next.js
    if not build_id:
        # Intentar algunos buildIds comunes (pueden cambiar, pero estos son ejemplos)
        possible_build_ids = ["ElfpMmIrFt5PD9X9NVWf7", "build", "latest"]
        print(f"DEBUG: [ADIDAS] No se encontró buildId, intentando valores comunes...", file=sys.stderr, flush=True)
        for bid in possible_build_ids:
            try:
                test_url = f"{ADIDAS_API_BASE}/_next/data/{bid}/{path_name}.json"
                test_response = session.get(test_url, timeout=10)
                if test_response.status_code == 200:
                    build_id = bid
                    print(f"DEBUG: [ADIDAS] BuildId funcional encontrado: {build_id}", file=sys.stderr, flush=True)
                    break
            except:
                continue
    
    while True:
        if max_pages and page > max_pages:
            print(f"DEBUG: Límite de páginas alcanzado ({max_pages}) para Adidas", file=sys.stderr, flush=True)
            break
        if page > MAX_PAGES_SAFETY:
            print(f"DEBUG: Límite de seguridad alcanzado ({MAX_PAGES_SAFETY} páginas) para Adidas", file=sys.stderr, flush=True)
            break
        
        try:
            # Si tenemos buildId, usar el endpoint JSON directamente
            if build_id:
                # Construir URL de la API JSON: /_next/data/{buildId}/{path}.json?params
                query_params = []
                if parsed.query:
                    # Mantener los parámetros originales
                    for param in parsed.query.split('&'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            if key != 'start':
                                query_params.append(f"{key}={value}")
                
                # Agregar start para paginación
                query_params.append(f"start={start_index}")
                
                api_url = f"{ADIDAS_API_BASE}/_next/data/{build_id}/{path_name}.json"
                if query_params:
                    api_url += "?" + "&".join(query_params)
                
                print(f"DEBUG: [ADIDAS] Página {page} - Consultando API JSON: {api_url}", file=sys.stderr, flush=True)
                
                # Obtener JSON directamente de la API
                response = session.get(api_url, timeout=30)
                print(f"DEBUG: [ADIDAS] Respuesta API JSON, status: {response.status_code}, tamaño: {len(response.text)} bytes", file=sys.stderr, flush=True)
                
                if response.status_code == 200:
                    try:
                        next_data = response.json()
                        print(f"DEBUG: [ADIDAS] JSON parseado correctamente. Claves: {list(next_data.keys())}", file=sys.stderr, flush=True)
                    except json.JSONDecodeError as e:
                        print(f"DEBUG: [ADIDAS] Error parseando JSON: {e}", file=sys.stderr, flush=True)
                        break
                elif response.status_code == 404:
                    print(f"DEBUG: [ADIDAS] 404 en API JSON, probablemente no hay más páginas", file=sys.stderr, flush=True)
                    break
                elif response.status_code == 403:
                    print(f"DEBUG: [ADIDAS] ⚠️ ERROR 403: Adidas bloquea la API JSON también", file=sys.stderr, flush=True)
                    break
                else:
                    print(f"DEBUG: [ADIDAS] Error HTTP {response.status_code}: {response.text[:500]}", file=sys.stderr, flush=True)
                    break
            else:
                # Si no hay buildId, intentar obtener desde HTML (método anterior como fallback)
                current_url = page_url
                if start_index > 0:
                    if 'start=' not in current_url:
                        separator = '&' if '?' in current_url else '?'
                        current_url += f"{separator}start={start_index}"
                    else:
                        current_url = re.sub(r'start=\d+', f'start={start_index}', current_url)
                
                print(f"DEBUG: [ADIDAS] Página {page} - Sin buildId, usando método HTML: {current_url}", file=sys.stderr, flush=True)
                response = session.get(current_url, timeout=30)
                print(f"DEBUG: [ADIDAS] Respuesta HTML, status: {response.status_code}", file=sys.stderr, flush=True)
                
                if response.status_code != 200:
                    print(f"DEBUG: [ADIDAS] Error HTTP {response.status_code}", file=sys.stderr, flush=True)
                    break
                
                # Extraer __NEXT_DATA__ del HTML
                next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', response.text, re.DOTALL)
                if not next_data_match:
                    print(f"DEBUG: [ADIDAS] No se encontró __NEXT_DATA__ en HTML", file=sys.stderr, flush=True)
                    break
                
                try:
                    next_data = json.loads(next_data_match.group(1))
                except json.JSONDecodeError as e:
                    print(f"DEBUG: [ADIDAS] Error parseando JSON del HTML: {e}", file=sys.stderr, flush=True)
                    break
            
            # Extraer productos de pageProps
            page_props = next_data.get("pageProps", {})
            if not page_props:
                print(f"DEBUG: [ADIDAS] ERROR: pageProps está vacío. Claves disponibles: {list(next_data.keys())}", file=sys.stderr, flush=True)
                break
            
            products = page_props.get("products", [])
            info = page_props.get("info", {})
            
            print(f"DEBUG: [ADIDAS] Productos encontrados en página {page}: {len(products) if products else 0}", file=sys.stderr, flush=True)
            
            if not products:
                print(f"DEBUG: [ADIDAS] Página {page} sin productos, deteniendo paginación", file=sys.stderr, flush=True)
                break
            
            # Agregar todos los productos (el filtro se hará después en procesar_productos_adidas)
            all_products.extend(products)
            print(f"DEBUG: [ADIDAS] Página {page}: {len(products)} productos encontrados (total acumulado: {len(all_products)})", file=sys.stderr, flush=True)
            
            # Verificar si hay más páginas
            total_count = info.get("count", 0)
            current_start = info.get("startIndex", start_index)
            view_size_from_info = info.get("viewSize", view_size)
            
            print(f"DEBUG: [ADIDAS] Info - Total: {total_count}, Start actual: {current_start}, Productos en página: {len(products)}, ViewSize: {view_size_from_info}", file=sys.stderr, flush=True)
            
            # Si no hay más productos o hemos alcanzado el total, detener
            if len(products) < view_size_from_info or (total_count > 0 and current_start + len(products) >= total_count):
                print(f"DEBUG: [ADIDAS] Última página detectada (solo {len(products)} productos en página {page}, total: {total_count})", file=sys.stderr, flush=True)
                break
            
            # Avanzar a la siguiente página
            start_index += view_size_from_info
            page += 1
            
            # Delay entre peticiones para evitar ser bloqueado (más tiempo para parecer humano)
            time.sleep(1.5)  # Esperar 1.5 segundos entre peticiones
                
        except requests.exceptions.Timeout:
            print(f"DEBUG: [ADIDAS] Timeout al obtener página {page}", file=sys.stderr, flush=True)
            break
        except requests.exceptions.RequestException as e:
            print(f"DEBUG: [ADIDAS] Error de petición en página {page}: {e}", file=sys.stderr, flush=True)
            break
        except Exception as e:
            print(f"DEBUG: [ADIDAS] Error inesperado en página {page}: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc()
            break
    
    print(f"DEBUG: [ADIDAS] Total de páginas procesadas: {page - 1}, Total productos: {len(all_products)}", file=sys.stderr, flush=True)
    return all_products

def procesar_productos_adidas(products, descuento_minimo=70):
    """Procesa productos de Adidas y los convierte al formato estándar"""
    productos = []
    productos_filtrados = 0
    productos_sin_precio = 0
    productos_sin_url = 0
    
    print(f"DEBUG: [ADIDAS PROCESAR] Procesando {len(products)} productos con descuento mínimo: {descuento_minimo}%", file=sys.stderr, flush=True)
    
    for idx, product in enumerate(products):
        if not isinstance(product, dict):
            continue
        
        # Extraer datos del producto
        nombre = product.get("title", "") or product.get("name", "")
        if not nombre:
            continue
        
        sub_title = product.get("subTitle", "")
        if sub_title:
            nombre = f"{nombre} - {sub_title}"
        
        # Extraer precios
        price_data = product.get("priceData", {})
        prices = price_data.get("prices", [])
        
        precio_original = None
        precio_promo = None
        descuento_num = 0
        
        # Buscar precios originales y de venta
        for price_item in prices:
            price_type = price_item.get("type", "")
            # Adidas usa valueNoVat o value
            price_value = price_item.get("valueNoVat") or price_item.get("value", 0)
            discount_pct = price_item.get("discountPercentage", 0)
            
            if price_type == "original":
                precio_original = price_value
                # Si hay descuento directo, usarlo
                if discount_pct > 0:
                    descuento_num = discount_pct
            elif price_type == "sale":
                precio_promo = price_value
        
        # Calcular descuento desde los precios si no se encontró directamente
        if descuento_num == 0 and precio_original and precio_promo and precio_original > precio_promo:
            descuento_num = ((precio_original - precio_promo) / precio_original) * 100
        # Si solo tenemos precio original pero no promocional, no hay descuento
        elif precio_original and not precio_promo:
            descuento_num = 0
        
        # Debug: mostrar información del producto
        if idx < 3:  # Solo los primeros 3 para no saturar
            print(f"DEBUG: [ADIDAS PROCESAR] Producto {idx+1}: {nombre[:50]}... - Original: {precio_original}, Promo: {precio_promo}, Descuento: {descuento_num:.1f}%", file=sys.stderr, flush=True)
        
        # Filtrar por descuento mínimo
        if descuento_num < descuento_minimo:
            productos_filtrados += 1
            if idx < 3:
                print(f"DEBUG: [ADIDAS PROCESAR] Producto {idx+1} filtrado: descuento {descuento_num:.1f}% < {descuento_minimo}%", file=sys.stderr, flush=True)
            continue
        
        # URL del producto
        url_path = product.get("url", "")
        if url_path:
            if url_path.startswith("/"):
                url = f"{ADIDAS_API_BASE}{url_path}"
            elif url_path.startswith("http"):
                url = url_path
            else:
                url = f"{ADIDAS_API_BASE}/{url_path}"
        else:
            productos_sin_url += 1
            if idx < 3:
                print(f"DEBUG: [ADIDAS PROCESAR] Producto {idx+1} sin URL", file=sys.stderr, flush=True)
            continue
        
        # Verificar que tengamos al menos un precio
        if not precio_original and not precio_promo:
            productos_sin_precio += 1
            if idx < 3:
                print(f"DEBUG: [ADIDAS PROCESAR] Producto {idx+1} sin precio", file=sys.stderr, flush=True)
            continue
        
        # Imagen del producto
        imagen_url = product.get("image", "") or product.get("hoverImage", "")
        if imagen_url and not imagen_url.startswith("http"):
            if imagen_url.startswith("//"):
                imagen_url = "https:" + imagen_url
            elif imagen_url.startswith("/"):
                imagen_url = ADIDAS_API_BASE + imagen_url
        
        # Marca (siempre Adidas)
        marca = "Adidas"
        
        # Formatear precios
        if precio_promo:
            precio_formateado = f"S/ {precio_promo:.2f}"
        elif precio_original:
            precio_formateado = f"S/ {precio_original:.2f}"
        else:
            precio_formateado = "No disponible"
        
        if precio_original:
            precio_real_formateado = f"S/ {precio_original:.2f}"
        else:
            precio_real_formateado = "No disponible"
        
        # Precio numérico para ordenar
        precio_num = precio_promo or precio_original or 0
        
        # Formatear descuento
        descuento = f"{descuento_num:.0f}%" if descuento_num > 0 else ""
        
        # Calcular valor descontado
        valor_descontado = 0
        if precio_original and precio_promo:
            valor_descontado = precio_original - precio_promo
        
        productos.append({
            "nombre": nombre,
            "marca": marca,
            "tienda": "Adidas",
            "precio_real": precio_real_formateado,
            "precio": precio_formateado,
            "precio_num": precio_num,
            "descuento": descuento,
            "descuento_num": descuento_num,
            "valor_descontado": valor_descontado,
            "url": url,
            "imagen": imagen_url
        })
    
    # Ordenar productos por precio de menor a mayor
    productos.sort(key=lambda x: x.get("precio_num", 0), reverse=False)
    
    print(f"DEBUG: [ADIDAS PROCESAR] Resumen:", file=sys.stderr, flush=True)
    print(f"  - Total productos recibidos: {len(products)}", file=sys.stderr, flush=True)
    print(f"  - Productos con descuento >= {descuento_minimo}%: {len(productos)}", file=sys.stderr, flush=True)
    print(f"  - Productos filtrados por descuento: {productos_filtrados}", file=sys.stderr, flush=True)
    print(f"  - Productos sin URL: {productos_sin_url}", file=sys.stderr, flush=True)
    print(f"  - Productos sin precio: {productos_sin_precio}", file=sys.stderr, flush=True)
    
    return productos

def procesar_json_adidas_directo(json_data, descuento_minimo=60):
    """Procesa un JSON de Adidas obtenido directamente (por ejemplo, desde el navegador)"""
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    
    page_props = json_data.get("pageProps", {})
    products = page_props.get("products", [])
    
    print(f"DEBUG: [ADIDAS JSON] Procesando {len(products)} productos desde JSON directo", file=sys.stderr, flush=True)
    return procesar_productos_adidas(products, descuento_minimo=descuento_minimo)

def leer_json_desde_archivo(ruta_archivo="adidas_data.json"):
    """Lee JSON de Adidas desde un archivo local"""
    import os
    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                # Si el contenido está dentro de <script> tags, extraerlo
                if '<script' in contenido:
                    match = re.search(r'<script[^>]*>(.*?)</script>', contenido, re.DOTALL)
                    if match:
                        contenido = match.group(1).strip()
                return json.loads(contenido)
        except Exception as e:
            print(f"DEBUG: [ADIDAS] Error leyendo archivo JSON: {e}", file=sys.stderr, flush=True)
            return None
    return None

def obtener_ofertas_adidas_por_categoria(categoria):
    """Obtiene productos de Adidas de una categoría específica"""
    url_path = categoria.get("url", "")
    descuento_minimo = categoria.get("descuento_minimo", 60)
    category_name = categoria.get("name", "Adidas")
    
    print(f"DEBUG: [ADIDAS CATEGORIA] Consultando Adidas: {category_name} (URL: {url_path}, Descuento mínimo: {descuento_minimo}%)", file=sys.stderr, flush=True)
    
    # Primero intentar leer JSON desde archivo local (si existe)
    json_data = leer_json_desde_archivo()
    if json_data:
        print(f"DEBUG: [ADIDAS CATEGORIA] ✅ JSON encontrado en archivo local, procesando...", file=sys.stderr, flush=True)
        try:
            productos = procesar_json_adidas_directo(json_data, descuento_minimo=descuento_minimo)
            print(f"DEBUG: [ADIDAS CATEGORIA] Productos procesados desde JSON: {len(productos)}", file=sys.stderr, flush=True)
            return {
                "categoria": category_name,
                "productos": productos
            }
        except Exception as e:
            print(f"DEBUG: [ADIDAS CATEGORIA] Error procesando JSON local: {e}", file=sys.stderr, flush=True)
            # Continuar con método normal si falla
    
    # Si no hay archivo local, intentar obtener desde la web
    try:
        print(f"DEBUG: [ADIDAS CATEGORIA] Llamando a obtener_productos_adidas...", file=sys.stderr, flush=True)
        products = obtener_productos_adidas(url_path, descuento_minimo=descuento_minimo)
        print(f"DEBUG: [ADIDAS CATEGORIA] Productos obtenidos: {len(products) if products else 0}", file=sys.stderr, flush=True)
        
        if not products:
            print(f"DEBUG: [ADIDAS CATEGORIA] No se obtuvieron productos, retornando lista vacía", file=sys.stderr, flush=True)
            print(f"DEBUG: [ADIDAS CATEGORIA] 📝 INSTRUCCIONES: Para usar JSON desde el navegador:", file=sys.stderr, flush=True)
            print(f"DEBUG: [ADIDAS CATEGORIA] 1. Abre https://www.adidas.pe/mujer?grid=true&sale_percentage_es_pe=50%7C55%7C60%7C70&sort=price-low-to-high", file=sys.stderr, flush=True)
            print(f"DEBUG: [ADIDAS CATEGORIA] 2. Presiona F12 (DevTools) > Network > Busca archivo .json o busca '__NEXT_DATA__' en la pestaña Sources", file=sys.stderr, flush=True)
            print(f"DEBUG: [ADIDAS CATEGORIA] 3. Copia el contenido JSON completo y guárdalo en un archivo llamado 'adidas_data.json' en el directorio del proyecto", file=sys.stderr, flush=True)
            print(f"DEBUG: [ADIDAS CATEGORIA] 4. Ejecuta la aplicación nuevamente", file=sys.stderr, flush=True)
            return {"categoria": category_name, "productos": []}
        
        print(f"DEBUG: [ADIDAS CATEGORIA] Procesando {len(products)} productos...", file=sys.stderr, flush=True)
        productos = procesar_productos_adidas(products, descuento_minimo=descuento_minimo)
        print(f"DEBUG: [ADIDAS CATEGORIA] Productos procesados: {len(productos)}", file=sys.stderr, flush=True)
        
        return {
            "categoria": category_name,
            "productos": productos
        }
        
    except Exception as e:
        print(f"DEBUG: [ADIDAS CATEGORIA] [ERROR] Error en {category_name}: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"categoria": category_name, "productos": []}

# ============================================================================
# FUNCIONES PARA FALABELLA (ORIGINALES)
# ============================================================================

def obtener_productos_de_categoria(category_id, category_name, max_pages=None, vendedores=None):
    """Obtiene productos de una categoría específica, iterando sobre múltiples páginas hasta que no haya más productos"""
    all_results = []
    headers = {
        "Accept": "application/json"
    }
    
    # Límite máximo de seguridad para evitar bucles infinitos (1000 páginas)
    MAX_PAGES_SAFETY = 1000
    page = 1
    
    while True:
        # Verificar límite de seguridad
        if max_pages and page > max_pages:
            break
        if page > MAX_PAGES_SAFETY:
            break
        
        params = {
            "sortBy": "derived.price.search,asc",
            "latLong": '{"latitude":"-12.0510554271","longitude":"-77.0490377322"}',
            "categoryId": category_id,
            "categoryName": category_name,
            "pgid": "2",
            "pid": "799c102f-9b4c-44be-a421-23e366a63b82",
            "zones": "PPE3630,IBIS_51,PPE3342,PPE3576,PPE4714,PPE1112,PPE3601,150100,PPE3627,PPE3628,912_LIMA_2,PPE1280,150000,PPE4,PPE3634,912_LIMA_1,PPE1279,150101,PPE344,PPE4726,IBIS_33,PPE2552,BATERIAS_AL_TOQUE,PPE4724,PPE2485,PPE4713,PPE3059,PPE3629,PPE2492,IMP_2,PPE3331,PPE1091,PERF_TEST,PPE1653,IBIS_99,PPE3578,OLVAA_81,PPE2815,IMP_1,PPE3164,3202,PPE3618,PPE4746,IBIS_110,PPE3659,PPE2918,IBIS_120,PPE4722,INT_CXP,PPE4684,URBANO_83,PPE2429,PPE3152,PPE4725,GARDEN_BY_DFZ,PPE4704,CHAPA_ESA_FLOR_DIRECTO,PPE4703,LIMA_URB1_DIRECTO,PPE2511,PPE4740",
            # Filtro para vendedores: usar el especificado o el predeterminado
            "f.derived.variant.sellerId": vendedores if vendedores else "FALABELLA::TOTTUS::SODIMAC",
            # Parámetro de paginación
            "page": str(page)
        }

        try:
            r = requests.get(API_URL, params=params, headers=headers, timeout=15)
            r.raise_for_status()
            response_data = r.json()
            
            # La nueva API devuelve los datos en data.results
            data = response_data.get("data", {})
            
            # Debug temporal: verificar estructura
            if not data.get("results"):
                # Intentar directamente en response_data
                if "results" in response_data:
                    data = response_data
            
            results = data.get("results", [])
            
            # Si no hay resultados, detener la paginación
            if not results:
                if page == 1:
                    print(f"DEBUG: [obtener_productos_de_categoria] Categoría '{category_name}' (ID: {category_id}): No se obtuvieron resultados en la primera página", file=sys.stderr, flush=True)
                break
            
            # Agregar información de categoría a cada producto
            for result in results:
                if isinstance(result, dict):
                    result["_categoria"] = category_name
                    result["_categoria_id"] = category_id
            
            all_results.extend(results)
            
            # Si recibimos menos productos de los esperados (típicamente 48), probablemente es la última página
            if len(results) < 48:
                break
            
            # Incrementar página para la siguiente iteración
            page += 1
                
        except requests.exceptions.Timeout:
            print(f"ERROR: [obtener_productos_de_categoria] Timeout para categoría '{category_name}' (ID: {category_id}) en página {page}", file=sys.stderr, flush=True)
            break  # Detener si hay timeout
        except requests.exceptions.RequestException as e:
            print(f"ERROR: [obtener_productos_de_categoria] Error de petición para categoría '{category_name}' (ID: {category_id}) en página {page}: {e}", file=sys.stderr, flush=True)
            break  # Detener si hay error
        except Exception as e:
            print(f"ERROR: [obtener_productos_de_categoria] Error inesperado para categoría '{category_name}' (ID: {category_id}) en página {page}: {e}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc(file=sys.stderr)
            break
    
    return all_results

def procesar_productos_de_categoria(results, category_name, marcas_omitir_adicionales=None, marca_especial=None, descuento_minimo=None):
    """Procesa los resultados de una categoría y devuelve productos filtrados"""
    productos = []
    productos_sin_filtro = 0
    productos_con_descuento_insuficiente = 0
    
    # Si hay marca especial y descuento mínimo, usar esos valores; si no, usar 50% por defecto
    descuento_requerido = descuento_minimo if descuento_minimo is not None else 60
    
    # Función recursiva para buscar texto de disponibilidad en toda la estructura
    def buscar_texto_disponibilidad(obj, path="", resultados=None):
        """Busca recursivamente texto relacionado con disponibilidad"""
        if resultados is None:
            resultados = []
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_path = f"{path}.{key}" if path else key
                if isinstance(value, (str, bool)):
                    texto = str(value).lower()
                    # Buscar textos relacionados con disponibilidad
                    if any(palabra in texto for palabra in ["retira", "disponible", "llega", "stock", "available"]):
                        resultados.append({
                            "path": current_path,
                            "value": value,
                            "type": type(value).__name__
                        })
                elif isinstance(value, (dict, list)):
                    buscar_texto_disponibilidad(value, current_path, resultados)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                buscar_texto_disponibilidad(item, f"{path}[{idx}]", resultados)
        
        return resultados
    
    # Marcas a omitir por defecto en Moda Mujer
    marcas_omitir_moda_mujer = []
    
    # Agregar marcas adicionales a omitir si se proporcionan
    if marcas_omitir_adicionales:
        marcas_omitir_moda_mujer.extend(marcas_omitir_adicionales)
    
    for item in results:
        if not isinstance(item, dict):
            continue
            
        nombre = item.get("displayName") or item.get("name") or item.get("productName")
        if not nombre:
            continue
        
        # Obtener marca del producto
        brand_data = item.get("brand")
        if isinstance(brand_data, dict):
            marca = brand_data.get("name") or brand_data.get("displayName") or ""
        elif isinstance(brand_data, str):
            marca = brand_data
        else:
            marca = item.get("brandName") or ""
        
        # Obtener categoría del producto
        categoria = item.get("_categoria", "")
        categoria_id = item.get("_categoria_id", "")
        
        # Obtener tienda/vendedor del producto
        tienda = ""
        seller_data = item.get("seller") or item.get("vendor") or item.get("sellerId") or item.get("sellerName")
        if isinstance(seller_data, dict):
            tienda = seller_data.get("name") or seller_data.get("displayName") or seller_data.get("id") or ""
        elif isinstance(seller_data, str):
            tienda = seller_data
        # Si no encontramos, buscar en variant o otros campos
        if not tienda:
            variant = item.get("variant") or item.get("variants", [])
            if isinstance(variant, dict):
                tienda = variant.get("sellerId") or variant.get("seller") or ""
            elif isinstance(variant, list) and len(variant) > 0:
                tienda = variant[0].get("sellerId") or variant[0].get("seller") or ""
        # Limpiar el nombre de la tienda (remover prefijos como "Por ")
        if tienda:
            tienda = tienda.replace("Por ", "").replace("por ", "").strip()
            # Si tiene formato FALABELLA::TOTTUS::SODIMAC, tomar solo el primero o formatear
            if "::" in tienda:
                tiendas_list = [t.strip() for t in tienda.split("::")]
                tienda = ", ".join(tiendas_list)
        
        # Si hay marca especial, filtrar solo productos de esa marca
        if marca_especial:
            if marca.upper() != marca_especial.upper():
                continue
        
        # Filtrar: en Moda Mujer, omitir productos de estas marcas (solo si no es categoría especial)
        if not marca_especial and (categoria == "Moda-Mujer" or categoria_id == "cat4100462") and marca.upper() in [m.upper() for m in marcas_omitir_moda_mujer]:
            continue
        
        # Filtrar: en Moda Hombre, omitir productos de la marca CURREN
        if (categoria == "Moda-Hombre" or categoria_id == "CATG12022") and marca.upper() == "CURREN":
            continue
        
        # Manejar prices - es una lista con objetos de precio
        prices_data = item.get("prices", [])
        precio_promo = None
        precio_original = None
        
        # Buscar descuento directo en el item (por si la API lo proporciona)
        descuento_directo = item.get("discount") or item.get("discountPercentage") or item.get("discountPercent")
        
        # Extraer precios de la lista
        if isinstance(prices_data, list):
            # Primera pasada: identificar todos los precios
            todos_precios = []
            for price_item in prices_data:
                if not isinstance(price_item, dict):
                    continue
                
                # El precio está en price[0]
                price_value = price_item.get("price", [])
                if isinstance(price_value, list) and len(price_value) > 0:
                    try:
                        precio_num = float(price_value[0])
                        price_type = price_item.get("type", "")
                        crossed = price_item.get("crossed", False)
                        
                        todos_precios.append({
                            "precio": precio_num,
                            "type": price_type,
                            "crossed": crossed
                        })
                        
                        # eventPrice o sin crossed es precio promocional
                        # normalPrice con crossed=True es precio original
                        if price_type == "eventPrice" or (not crossed and price_type != "normalPrice"):
                            if precio_promo is None or precio_num < precio_promo:  # Tomar el menor como promocional
                                precio_promo = precio_num
                        elif price_type == "normalPrice" and crossed:
                            if precio_original is None or precio_num > precio_original:  # Tomar el mayor como original
                                precio_original = precio_num
                    except (ValueError, TypeError):
                        continue
            
            # Si tenemos múltiples precios, ordenarlos y tomar el mayor como original y el menor como promocional
            if len(todos_precios) > 1:
                precios_ordenados = sorted([p["precio"] for p in todos_precios], reverse=True)
                # El mayor precio es el original
                precio_original = precios_ordenados[0]
                # El menor precio es el promocional
                precio_promo = precios_ordenados[-1]
            # Si no encontramos precio original pero sí promocional, buscar el mayor precio diferente
            elif precio_promo and not precio_original:
                for precio_info in todos_precios:
                    precio_num = precio_info["precio"]
                    crossed = precio_info["crossed"]
                    # Si está tachado o es diferente y mayor al precio promocional
                    if (crossed or (precio_num != precio_promo and precio_num > precio_promo)):
                        precio_original = precio_num
                        break
                
                # Si aún no encontramos, buscar el mayor precio de todos
                if not precio_original and todos_precios:
                    precios_ordenados = sorted([p["precio"] for p in todos_precios], reverse=True)
                    if len(precios_ordenados) > 1:
                        precio_original = precios_ordenados[0]
                        if precio_promo == precios_ordenados[0]:
                            precio_promo = precios_ordenados[1] if len(precios_ordenados) > 1 else precio_promo
        
        # Precio a mostrar (precio promocional o el único disponible)
        precio = precio_promo or precio_original
        
        # Calcular descuento desde precios
        descuento_num = 0
        valor_descontado = 0  # Valor absoluto del descuento
        
        # Si hay descuento directo, usarlo
        if descuento_directo:
            try:
                descuento_num = float(descuento_directo)
                if descuento_num > 100:  # Si viene como porcentaje (ej: 50 en lugar de 0.5)
                    descuento_num = descuento_num / 100 * 100 if descuento_num <= 1 else descuento_num
            except (ValueError, TypeError):
                pass
        
        # Si no hay descuento directo, calcularlo desde precios
        if descuento_num == 0 and precio_original and precio_promo and precio_original > precio_promo:
            try:
                precio_orig = float(precio_original)
                precio_pro = float(precio_promo)
                if precio_orig > 0:
                    descuento_num = ((precio_orig - precio_pro) / precio_orig) * 100
                    valor_descontado = precio_orig - precio_pro  # Calcular valor descontado
            except (ValueError, TypeError):
                descuento_num = 0
                valor_descontado = 0
        
        # Debug: si el producto tiene descuento pero no se detectó correctamente
        if descuento_num == 0 and precio_promo and precio_original and precio_original > precio_promo:
            descuento_calculado = ((precio_original - precio_promo) / precio_original) * 100
            # Forzar el cálculo del descuento si no se detectó
            descuento_num = descuento_calculado
            valor_descontado = precio_original - precio_promo

        # URL SEO del producto
        url = item.get("seoURL") or item.get("productSeoURL") or item.get("url") or item.get("productURL")
        if url and url.startswith("/"):
            url = "https://www.falabella.com.pe" + url
        elif not url:
            continue
        
        # Extraer imagen del producto
        imagen_url = None
        
        # Intentar varios campos comunes donde puede estar la imagen
        # PRIORIDAD 1: mediaUrls (campo específico de Falabella)
        if item.get("mediaUrls") and isinstance(item.get("mediaUrls"), list) and len(item["mediaUrls"]) > 0:
            imagen_url = item["mediaUrls"][0]  # Tomar la primera imagen
        elif item.get("images") and isinstance(item.get("images"), list) and len(item["images"]) > 0:
            # Si es lista, tomar la primera
            imagen_data = item["images"][0]
            if isinstance(imagen_data, dict):
                imagen_url = imagen_data.get("url") or imagen_data.get("src") or imagen_data.get("imageUrl") or imagen_data.get("uri")
            elif isinstance(imagen_data, str):
                imagen_url = imagen_data
        elif item.get("image"):
            imagen_data = item["image"]
            if isinstance(imagen_data, dict):
                imagen_url = imagen_data.get("url") or imagen_data.get("src") or imagen_data.get("imageUrl") or imagen_data.get("uri")
            elif isinstance(imagen_data, str):
                imagen_url = imagen_data
        elif item.get("thumbnail"):
            imagen_data = item["thumbnail"]
            if isinstance(imagen_data, dict):
                imagen_url = imagen_data.get("url") or imagen_data.get("src") or imagen_data.get("imageUrl") or imagen_data.get("uri")
            elif isinstance(imagen_data, str):
                imagen_url = imagen_data
        elif item.get("productImage"):
            imagen_data = item["productImage"]
            if isinstance(imagen_data, dict):
                imagen_url = imagen_data.get("url") or imagen_data.get("src") or imagen_data.get("imageUrl") or imagen_data.get("uri")
            elif isinstance(imagen_data, str):
                imagen_url = imagen_data
        elif item.get("media") and isinstance(item.get("media"), list) and len(item["media"]) > 0:
            imagen_data = item["media"][0]
            if isinstance(imagen_data, dict):
                imagen_url = imagen_data.get("url") or imagen_data.get("src") or imagen_data.get("imageUrl") or imagen_data.get("uri")
            elif isinstance(imagen_data, str):
                imagen_url = imagen_data
        elif item.get("primaryImage"):
            imagen_data = item["primaryImage"]
            if isinstance(imagen_data, dict):
                imagen_url = imagen_data.get("url") or imagen_data.get("src") or imagen_data.get("imageUrl") or imagen_data.get("uri")
            elif isinstance(imagen_data, str):
                imagen_url = imagen_data
        # Buscar en otros campos posibles
        elif item.get("gallery") and isinstance(item.get("gallery"), list) and len(item["gallery"]) > 0:
            imagen_data = item["gallery"][0]
            if isinstance(imagen_data, dict):
                imagen_url = imagen_data.get("url") or imagen_data.get("src") or imagen_data.get("imageUrl") or imagen_data.get("uri")
            elif isinstance(imagen_data, str):
                imagen_url = imagen_data
        elif item.get("productImages") and isinstance(item.get("productImages"), list) and len(item["productImages"]) > 0:
            imagen_data = item["productImages"][0]
            if isinstance(imagen_data, dict):
                imagen_url = imagen_data.get("url") or imagen_data.get("src") or imagen_data.get("imageUrl") or imagen_data.get("uri")
            elif isinstance(imagen_data, str):
                imagen_url = imagen_data
        
        # Si la URL es relativa, convertirla a absoluta
        if imagen_url and imagen_url.startswith("/"):
            imagen_url = "https://www.falabella.com.pe" + imagen_url
        elif imagen_url and not imagen_url.startswith("http"):
            # Si no tiene protocolo pero tampoco empieza con /, agregar https://
            if not imagen_url.startswith("//"):
                imagen_url = "https://" + imagen_url.lstrip("/")
        
        # Contador de productos válidos (con nombre y URL)
        productos_sin_filtro += 1
        
        # Verificar disponibilidad del producto
        # Buscar texto de disponibilidad en toda la estructura del producto
        campos_disponibilidad = buscar_texto_disponibilidad(item)
        
        disponible = False
        disponibilidad_texto = None
        
        # Buscar textos que indiquen disponibilidad (más flexibles)
        textos_disponible = ["retira hoy", "retira mañana", "retira", "llega hoy", "llega mañana", "llega", "disponible", "en stock", "available"]
        textos_no_disponible = ["no disponible", "sin stock", "agotado", "out of stock", "no disponible para"]
        
        # Revisar todos los campos encontrados
        for campo in campos_disponibilidad:
            valor_str = str(campo["value"]).lower()
            
            # Si encontramos un texto de "no disponible", el producto no está disponible
            if any(texto in valor_str for texto in textos_no_disponible):
                disponible = False
                disponibilidad_texto = campo["value"]
                break
            
            # Si encontramos un texto de disponibilidad positiva
            if any(texto in valor_str for texto in textos_disponible):
                disponible = True
                disponibilidad_texto = campo["value"]
                # No hacer break aquí, seguir buscando por si hay un "no disponible" después
        
        # Si no encontramos ningún campo de disponibilidad, intentar buscar en campos comunes
        if not campos_disponibilidad:
            # Buscar en campos comunes donde puede estar la disponibilidad
            campos_comunes = ["availability", "stock", "delivery", "pickup", "shipping", "disponibilidad", "entrega"]
            for campo_key in campos_comunes:
                valor = item.get(campo_key)
                if valor:
                    valor_str = str(valor).lower()
                    if any(texto in valor_str for texto in textos_disponible):
                        disponible = True
                        disponibilidad_texto = valor
                        break
                    elif any(texto in valor_str for texto in textos_no_disponible):
                        disponible = False
                        disponibilidad_texto = valor
                        break
        
        # Si aún no encontramos disponibilidad, pero tenemos precio y descuento válido, asumir disponible
        # (algunos productos pueden no tener el campo de disponibilidad pero estar disponibles)
        if not disponible and not campos_disponibilidad and precio and descuento_num > 0:
            disponible = True
            disponibilidad_texto = "Asumido disponible (tiene precio y descuento)"
        
        # Filtrar productos no disponibles (solo si definitivamente no están disponibles)
        if not disponible and campos_disponibilidad:
            print(f"DEBUG: Producto no disponible omitido: {nombre[:50]}... (disponibilidad: {disponibilidad_texto})", file=sys.stderr, flush=True)
            continue
        elif not disponible and not campos_disponibilidad:
            print(f"DEBUG: Producto sin campo de disponibilidad omitido: {nombre[:50]}... (precio: {precio}, descuento: {descuento_num:.1f}%)", file=sys.stderr, flush=True)
            continue
        
        # Filtrar productos según el descuento requerido (50% por defecto, o el especificado)
        # Usar >= para incluir productos con exactamente el descuento requerido
        if descuento_num < descuento_requerido:
            productos_con_descuento_insuficiente += 1
            continue
        
        # Debug: mostrar productos que SÍ pasan el filtro
        if descuento_num >= descuento_requerido:
            print(f"DEBUG: [PRODUCTO ACEPTADO] {nombre[:50]}... - Descuento: {descuento_num:.1f}% - Original: {precio_original}, Promo: {precio_promo}, Disponible: {disponible}", file=sys.stderr, flush=True)
        
        # Formatear descuento para mostrar
        descuento = f"{descuento_num:.0f}%" if descuento_num > 0 else ""
        
        # Formatear precio con descuento (precio promocional)
        if precio:
            precio_formateado = f"S/ {precio:.2f}"
        else:
            precio_formateado = "No disponible"
        
        # Formatear precio real (precio original)
        if precio_original:
            precio_real_formateado = f"S/ {precio_original:.2f}"
        else:
            precio_real_formateado = "No disponible"

        productos.append({
            "nombre": nombre,
            "marca": marca,
            "tienda": tienda or "Falabella",  # Valor por defecto si no se encuentra
            "precio_real": precio_real_formateado,
            "precio": precio_formateado,
            "precio_num": precio or 0,  # Precio numérico para ordenar
            "descuento": descuento,
            "descuento_num": descuento_num,
            "valor_descontado": valor_descontado,  # Agregar valor descontado
            "url": url,
            "imagen": imagen_url  # Agregar imagen
        })

    # Ordenar productos por precio de menor a mayor
    productos.sort(key=lambda x: x.get("precio_num", 0), reverse=False)
    
    print(f"DEBUG: [{category_name}] Productos procesados: {productos_sin_filtro}, con descuento > {descuento_requerido}%: {len(productos)}", file=sys.stderr, flush=True)
    print(f"DEBUG: Top 5 productos por precio (menor a mayor):", file=sys.stderr, flush=True)
    for i, p in enumerate(productos[:5], 1):
        print(f"  {i}. {p['marca']} - {p['nombre'][:40]}... - Precio: {p.get('precio', 'N/A')}", file=sys.stderr, flush=True)
    
    return productos

def obtener_ofertas_por_categoria(categoria):
    """Obtiene productos de una categoría específica y los devuelve agrupados"""
    # Verificar si es una categoría de Adidas
    if categoria.get("tipo") == "adidas":
        return obtener_ofertas_adidas_por_categoria(categoria)
    
    # Si no es Adidas, usar las funciones de Falabella
    category_id = categoria["id"]
    category_name = categoria["name"]
    marcas_omitir = categoria.get("marcas_omitir", None)
    marca_especial = categoria.get("marca_especial", None)
    descuento_minimo = categoria.get("descuento_minimo", None)
    categoria_base = categoria.get("categoria_base", category_name)
    vendedores = categoria.get("vendedores", None)
    
    try:
        # Si hay categoria_base, usar esa para obtener productos, pero procesar con el nombre especial
        category_name_for_api = categoria_base if categoria_base else category_name
        print(f"DEBUG: [obtener_ofertas_por_categoria] Obteniendo productos para categoría '{category_name}' (ID: {category_id}, nombre API: '{category_name_for_api}')", file=sys.stderr, flush=True)
        results = obtener_productos_de_categoria(category_id, category_name_for_api, vendedores=vendedores)
        print(f"DEBUG: [obtener_ofertas_por_categoria] Categoría '{category_name}': {len(results)} resultados obtenidos", file=sys.stderr, flush=True)
        if not results:
            print(f"DEBUG: [obtener_ofertas_por_categoria] Categoría '{category_name}': No se obtuvieron resultados", file=sys.stderr, flush=True)
            return {"categoria": category_name, "productos": []}
        
        productos = procesar_productos_de_categoria(
            results, 
            category_name, 
            marcas_omitir_adicionales=marcas_omitir,
            marca_especial=marca_especial,
            descuento_minimo=descuento_minimo
        )
        
        print(f"DEBUG: [obtener_ofertas_por_categoria] Categoría '{category_name}': {len(productos)} productos procesados", file=sys.stderr, flush=True)
        
        return {
            "categoria": category_name,
            "productos": productos
        }
        
    except Exception as e:
        print(f"ERROR: [obtener_ofertas_por_categoria] Error procesando categoría '{category_name}' (ID: {category_id}): {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"categoria": category_name, "productos": []}

def obtener_ofertas():
    # Obtener productos de todas las categorías
    all_results = []
    
    for i, categoria in enumerate(CATEGORIAS, 1):
        try:
            results = obtener_productos_de_categoria(categoria["id"], categoria["name"])
            all_results.extend(results)
        except Exception as e:
            pass
    
    if len(all_results) == 0:
        return []
    
    productos = []
    productos_sin_filtro = 0
    productos_con_descuento_insuficiente = 0
    productos_por_categoria = {}  # Contador por categoría
    
    # Usar todos los resultados combinados
    for item in all_results:
        if not isinstance(item, dict):
            continue
            
        nombre = item.get("displayName") or item.get("name") or item.get("productName")
        if not nombre:
            continue
        
        # Obtener marca del producto
        brand_data = item.get("brand")
        if isinstance(brand_data, dict):
            marca = brand_data.get("name") or brand_data.get("displayName") or ""
        elif isinstance(brand_data, str):
            marca = brand_data
        else:
            marca = item.get("brandName") or ""
        
        # Obtener categoría del producto
        categoria = item.get("_categoria", "")
        categoria_id = item.get("_categoria_id", "")
        
        # Obtener tienda/vendedor del producto
        tienda = ""
        seller_data = item.get("seller") or item.get("vendor") or item.get("sellerId") or item.get("sellerName")
        if isinstance(seller_data, dict):
            tienda = seller_data.get("name") or seller_data.get("displayName") or seller_data.get("id") or ""
        elif isinstance(seller_data, str):
            tienda = seller_data
        # Si no encontramos, buscar en variant o otros campos
        if not tienda:
            variant = item.get("variant") or item.get("variants", [])
            if isinstance(variant, dict):
                tienda = variant.get("sellerId") or variant.get("seller") or ""
            elif isinstance(variant, list) and len(variant) > 0:
                tienda = variant[0].get("sellerId") or variant[0].get("seller") or ""
        # Limpiar el nombre de la tienda (remover prefijos como "Por ")
        if tienda:
            tienda = tienda.replace("Por ", "").replace("por ", "").strip()
            # Si tiene formato FALABELLA::TOTTUS::SODIMAC, tomar solo el primero o formatear
            if "::" in tienda:
                tiendas_list = [t.strip() for t in tienda.split("::")]
                tienda = ", ".join(tiendas_list)
        
        # Marcas a omitir en Moda Mujer
        marcas_omitir_moda_mujer = []
        
        # Filtrar: en Moda Mujer, omitir productos de estas marcas
        if (categoria == "Moda-Mujer" or categoria_id == "cat4100462") and marca.upper() in [m.upper() for m in marcas_omitir_moda_mujer]:
            continue
        
        # Filtrar: en Moda Hombre, omitir productos de la marca CURREN
        if (categoria == "Moda-Hombre" or categoria_id == "CATG12022") and marca.upper() == "CURREN":
            continue
        
        # Manejar prices - es una lista con objetos de precio
        prices_data = item.get("prices", [])
        precio_promo = None
        precio_original = None
        
        # Buscar descuento directo en el item (por si la API lo proporciona)
        descuento_directo = item.get("discount") or item.get("discountPercentage") or item.get("discountPercent")
        
        # Extraer precios de la lista
        if isinstance(prices_data, list):
            # Primera pasada: identificar todos los precios
            todos_precios = []
            for price_item in prices_data:
                if not isinstance(price_item, dict):
                    continue
                
                # El precio está en price[0]
                price_value = price_item.get("price", [])
                if isinstance(price_value, list) and len(price_value) > 0:
                    try:
                        precio_num = float(price_value[0])
                        price_type = price_item.get("type", "")
                        crossed = price_item.get("crossed", False)
                        
                        todos_precios.append({
                            "precio": precio_num,
                            "type": price_type,
                            "crossed": crossed
                        })
                        
                        # eventPrice o sin crossed es precio promocional
                        # normalPrice con crossed=True es precio original
                        if price_type == "eventPrice" or (not crossed and price_type != "normalPrice"):
                            if precio_promo is None or precio_num < precio_promo:  # Tomar el menor como promocional
                                precio_promo = precio_num
                        elif price_type == "normalPrice" and crossed:
                            if precio_original is None or precio_num > precio_original:  # Tomar el mayor como original
                                precio_original = precio_num
                    except (ValueError, TypeError):
                        continue
            
            # Si tenemos múltiples precios, ordenarlos y tomar el mayor como original y el menor como promocional
            if len(todos_precios) > 1:
                precios_ordenados = sorted([p["precio"] for p in todos_precios], reverse=True)
                # El mayor precio es el original
                precio_original = precios_ordenados[0]
                # El menor precio es el promocional
                precio_promo = precios_ordenados[-1]
            # Si no encontramos precio original pero sí promocional, buscar el mayor precio diferente
            elif precio_promo and not precio_original:
                for precio_info in todos_precios:
                    precio_num = precio_info["precio"]
                    crossed = precio_info["crossed"]
                    # Si está tachado o es diferente y mayor al precio promocional
                    if (crossed or (precio_num != precio_promo and precio_num > precio_promo)):
                        precio_original = precio_num
                        break
                
                # Si aún no encontramos, buscar el mayor precio de todos
                if not precio_original and todos_precios:
                    precios_ordenados = sorted([p["precio"] for p in todos_precios], reverse=True)
                    if len(precios_ordenados) > 1:
                        precio_original = precios_ordenados[0]
                        if precio_promo == precios_ordenados[0]:
                            precio_promo = precios_ordenados[1] if len(precios_ordenados) > 1 else precio_promo
        
        # Precio a mostrar (precio promocional o el único disponible)
        precio = precio_promo or precio_original
        
        # Calcular descuento desde precios
        descuento_num = 0
        
        # Si hay descuento directo, usarlo
        if descuento_directo:
            try:
                descuento_num = float(descuento_directo)
                if descuento_num > 100:  # Si viene como porcentaje (ej: 50 en lugar de 0.5)
                    descuento_num = descuento_num / 100 * 100 if descuento_num <= 1 else descuento_num
            except (ValueError, TypeError):
                pass
        
        # Si no hay descuento directo, calcularlo desde precios
        if descuento_num == 0 and precio_original and precio_promo and precio_original > precio_promo:
            try:
                precio_orig = float(precio_original)
                precio_pro = float(precio_promo)
                if precio_orig > 0:
                    descuento_num = ((precio_orig - precio_pro) / precio_orig) * 100
            except (ValueError, TypeError):
                descuento_num = 0

        # URL SEO del producto
        url = item.get("seoURL") or item.get("productSeoURL") or item.get("url") or item.get("productURL")
        if url and url.startswith("/"):
            url = "https://www.falabella.com.pe" + url
        elif not url:
            continue
        
        # Contador de productos válidos (con nombre y URL)
        productos_sin_filtro += 1
        
        # Contar por categoría
        cat_key = categoria or categoria_id or "Sin categoría"
        if cat_key not in productos_por_categoria:
            productos_por_categoria[cat_key] = {"total": 0, "con_descuento": 0}
        productos_por_categoria[cat_key]["total"] += 1
        
        # Filtrar solo productos con >= 50% de descuento (cambiar <= a < para incluir exactamente 50%)
        if descuento_num < 50:
            productos_con_descuento_insuficiente += 1
            continue
        
        # Contar productos con descuento > 60% por categoría
        productos_por_categoria[cat_key]["con_descuento"] += 1
        
        # Formatear descuento para mostrar
        descuento = f"{descuento_num:.0f}%" if descuento_num > 0 else ""
        
        # Formatear precio con descuento (precio promocional)
        if precio:
            precio_formateado = f"S/ {precio:.2f}"
        else:
            precio_formateado = "No disponible"
        
        # Formatear precio real (precio original)
        if precio_original:
            precio_real_formateado = f"S/ {precio_original:.2f}"
        else:
            precio_real_formateado = "No disponible"

        productos.append({
            "nombre": nombre,
            "marca": marca,
            "tienda": tienda or "Falabella",  # Valor por defecto si no se encuentra
            "precio_real": precio_real_formateado,  # Precio original
            "precio": precio_formateado,  # Precio con descuento
            "precio_num": precio or 0,  # Precio numérico para ordenar
            "descuento": descuento,
            "descuento_num": descuento_num,  # Guardar el número para ordenar
            "url": url
        })

    # Ordenar productos por precio de menor a mayor
    productos.sort(key=lambda x: x.get("precio_num", 0), reverse=False)
    
    return productos
