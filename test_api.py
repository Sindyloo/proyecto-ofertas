import requests
import json

API_URL = "https://www.falabella.com.pe/s/browse/v1/listing/pe"

params = {
    "sortBy": "derived.price.search,asc",
    "latLong": '{"latitude":"-12.0510554271","longitude":"-77.0490377322"}',
    "categoryId": "cat4100462",
    "categoryName": "Moda-Mujer",
    "pgid": "2",
    "pid": "799c102f-9b4c-44be-a421-23e366a63b82",
    "f.derived.variant.sellerId": "FALABELLA::TOTTUS",
    "zones": "PPE3630,IBIS_51,PPE3342,PPE3576,PPE4714,PPE1112,PPE3601,150100,PPE3627,PPE3628,912_LIMA_2,PPE1280,150000,PPE4,PPE3634,912_LIMA_1,PPE1279,150101,PPE344,PPE4726,IBIS_33,PPE2552,BATERIAS_AL_TOQUE,PPE4724,PPE2485,PPE4713,PPE3059,PPE3629,PPE2492,IMP_2,PPE3331,PPE1091,PERF_TEST,PPE1653,IBIS_99,PPE3578,OLVAA_81,PPE2815,IMP_1,PPE3164,3202,PPE3618,PPE4746,IBIS_110,PPE3659,PPE2918,IBIS_120,PPE4722,INT_CXP,PPE4684,URBANO_83,PPE2429,PPE3152,PPE4725,GARDEN_BY_DFZ,PPE4704,CHAPA_ESA_FLOR_DIRECTO,PPE4703,LIMA_URB1_DIRECTO,PPE2511,PPE4740"
}

headers = {
    "Accept": "application/json"
}

print("=" * 60)
print("PRUEBA DE API DE FALABELLA")
print("=" * 60)

try:
    print("\n1. Haciendo petición a la API...")
    r = requests.get(API_URL, params=params, headers=headers)
    print(f"   Status code: {r.status_code}")
    
    if r.status_code != 200:
        print(f"   ERROR: Status code {r.status_code}")
        print(f"   Respuesta: {r.text[:500]}")
        exit(1)
    
    print("2. Parseando respuesta JSON...")
    response_data = r.json()
    
    print(f"3. Claves en la respuesta principal: {list(response_data.keys())[:10]}")
    
    # Buscar resultados
    data = response_data.get("data", {})
    print(f"4. Claves en 'data': {list(data.keys())[:10] if isinstance(data, dict) else 'No es dict'}")
    
    results = data.get("results", []) if isinstance(data, dict) else []
    if not results:
        results = response_data.get("results", [])
    
    print(f"5. Total de resultados encontrados: {len(results)}")
    
    if len(results) == 0:
        print("\n   ⚠️  No se encontraron resultados")
        print("\n   Estructura completa de la respuesta:")
        print("   " + "-" * 56)
        import json
        print(json.dumps(response_data, indent=2)[:1000])
        exit(1)
    
    print(f"\n6. Analizando primer producto como ejemplo:")
    print("   " + "-" * 56)
    
    primer_item = results[0]
    if isinstance(primer_item, dict):
        print(f"   Claves en primer item: {list(primer_item.keys())[:15]}")
        
        nombre = primer_item.get("displayName") or primer_item.get("name") or primer_item.get("productName")
        print(f"   Nombre: {nombre}")
        
        prices_data = primer_item.get("prices")
        print(f"   Tipo de prices: {type(prices_data)}")
        
        # Mostrar estructura completa de prices
        if isinstance(prices_data, list):
            print(f"   prices es una lista con {len(prices_data)} elementos:")
            for i, price_item in enumerate(prices_data):
                print(f"   [{i}]: {json.dumps(price_item, indent=6, ensure_ascii=False)}")
        elif isinstance(prices_data, dict):
            print(f"   prices es un diccionario:")
            print(f"   {json.dumps(prices_data, indent=6, ensure_ascii=False)}")
        else:
            print(f"   prices: {prices_data}")
        
        # Intentar extraer precios
        if isinstance(prices_data, list) and len(prices_data) > 0:
            print(f"\n   Intentando extraer precios:")
            for price_item in prices_data:
                price_type = price_item.get("type", "")
                price_value = price_item.get("price", [])
                price_value_str = price_value[0] if isinstance(price_value, list) and len(price_value) > 0 else price_value
                print(f"   - Tipo: {price_type}, Precio: {price_value_str}, Cruzado: {price_item.get('crossed', False)}")
                
        # Calcular descuento
        if isinstance(prices_data, dict):
            precio_promo = prices_data.get("promoPrice") or prices_data.get("currentPrice")
            precio_original = prices_data.get("listPrice") or prices_data.get("originalPrice")
            
            print(f"   Precio promocional: {precio_promo}")
            print(f"   Precio original: {precio_original}")
            
            if precio_original and precio_promo:
                try:
                    descuento = ((float(precio_original) - float(precio_promo)) / float(precio_original)) * 100
                    print(f"   Descuento calculado: {descuento:.2f}%")
                except:
                    print("   No se pudo calcular descuento")
    
    # Contar productos con descuento > 60%
    print(f"\n7. Filtrando productos con descuento > 60%:")
    print("   " + "-" * 56)
    
    productos_con_descuento_alto = 0
    for item in results[:10]:  # Solo primeros 10 para prueba
        if not isinstance(item, dict):
            continue
        
        prices_data = item.get("prices")
        if isinstance(prices_data, list) and len(prices_data) > 0:
            prices_data = prices_data[0]
        
        if isinstance(prices_data, dict):
            precio_promo = prices_data.get("promoPrice") or prices_data.get("currentPrice")
            precio_original = prices_data.get("listPrice") or prices_data.get("originalPrice")
            
            if precio_original and precio_promo:
                try:
                    descuento = ((float(precio_original) - float(precio_promo)) / float(precio_original)) * 100
                    if descuento > 60:
                        productos_con_descuento_alto += 1
                        nombre = item.get("displayName") or item.get("name")
                        print(f"   [OK] {nombre}: {descuento:.1f}%")
                except:
                    pass
    
    print(f"\n   Total de productos con > 60% de descuento (primeros 10): {productos_con_descuento_alto}")
    
    # Buscar campos de stock/disponibilidad
    print("\n" + "=" * 60)
    print("BUSCANDO CAMPOS DE STOCK/DISPONIBILIDAD")
    print("=" * 60)
    
    if len(results) > 0:
        primer_item = results[0]
        
        print(f"\n1. Todas las claves del primer producto:")
        for key in primer_item.keys():
            print(f"   - {key}")
        
        print(f"\n2. Campos relacionados con stock/disponibilidad:")
        encontrados = False
        for key in primer_item.keys():
            key_lower = key.lower()
            if any(word in key_lower for word in ['stock', 'available', 'inventory', 'quantity', 'dispon', 'outofstock', 'instock', 'hasstock', 'availability']):
                encontrados = True
                valor = primer_item[key]
                print(f"   [ENCONTRADO] {key}: {valor} (tipo: {type(valor).__name__})")
                if isinstance(valor, dict):
                    print(f"      Estructura: {json.dumps(valor, indent=8, ensure_ascii=False)[:300]}")
        
        if not encontrados:
            print("   No se encontraron campos obvios con esas palabras")
        
        # Revisar específicamente el campo 'availability'
        print(f"\n2b. Análisis detallado del campo 'availability':")
        availability = primer_item.get('availability')
        print(f"   availability: {availability}")
        if isinstance(availability, dict):
            print(f"   Claves en availability: {list(availability.keys())}")
            for key, value in availability.items():
                print(f"   - {key}: {value}")
        elif isinstance(availability, list):
            print(f"   availability es una lista con {len(availability)} elementos")
            for i, item in enumerate(availability[:3]):  # Primeros 3
                print(f"   [{i}]: {item}")
        
        print(f"\n3. Badges y Stickers (pueden indicar 'sin stock'):")
        badges = primer_item.get('badges', [])
        print(f"   badges: {badges}")
        
        discount_badge = primer_item.get('discountBadge', '')
        print(f"   discountBadge: {discount_badge}")
        
        meat_stickers = primer_item.get('meatStickers', [])
        print(f"   meatStickers: {meat_stickers}")
        
        multipurpose_badges = primer_item.get('multipurposeBadges', [])
        print(f"   multipurposeBadges: {multipurpose_badges}")
        
        # Analizar el campo availability en varios productos
        print(f"\n4. Analizando campo 'availability' en varios productos:")
        productos_con_stock = 0
        productos_sin_stock = 0
        for i, item in enumerate(results[:20]):  # Primeros 20 productos
            nombre = item.get("displayName", "")[:50]
            availability = item.get("availability")
            
            # Analizar availability
            if isinstance(availability, dict):
                available = availability.get("available", availability.get("inStock", availability.get("hasStock")))
                if available is False or (isinstance(available, (int, float)) and available <= 0):
                    productos_sin_stock += 1
                    print(f"   [SIN STOCK] {nombre}: availability = {availability}")
                else:
                    productos_con_stock += 1
            elif isinstance(availability, list):
                # Si es lista, verificar si tiene elementos que indiquen disponibilidad
                disponible_en_lista = any(
                    (isinstance(a, dict) and a.get("available", True) is not False) or
                    (isinstance(a, bool) and a is True)
                    for a in availability
                )
                if not disponible_en_lista:
                    productos_sin_stock += 1
                    print(f"   [SIN STOCK] {nombre}: availability = {availability}")
                else:
                    productos_con_stock += 1
            elif availability is False or availability is None:
                productos_sin_stock += 1
                print(f"   ⚠ {nombre}: availability = {availability}")
            else:
                productos_con_stock += 1
        
        print(f"\n   Productos CON stock (primeros 20): {productos_con_stock}")
        print(f"   Productos SIN stock (primeros 20): {productos_sin_stock}")
    
    # Analizar campos de imagen
    print("\n" + "=" * 60)
    print("ANALIZANDO CAMPOS DE IMAGEN")
    print("=" * 60)
    
    if len(results) > 0:
        primer_item = results[0]
        
        print(f"\n1. Campo 'media':")
        media = primer_item.get('media')
        print(f"   Tipo: {type(media).__name__}")
        if isinstance(media, list):
            print(f"   Es una lista con {len(media)} elementos")
            if len(media) > 0:
                print(f"   Primer elemento: {json.dumps(media[0], indent=6, ensure_ascii=False)}")
        elif isinstance(media, dict):
            print(f"   Es un diccionario:")
            print(f"   {json.dumps(media, indent=6, ensure_ascii=False)}")
        else:
            print(f"   Valor: {media}")
        
        print(f"\n2. Campo 'mediaUrls':")
        mediaUrls = primer_item.get('mediaUrls')
        print(f"   Tipo: {type(mediaUrls).__name__}")
        if isinstance(mediaUrls, list):
            print(f"   Es una lista con {len(mediaUrls)} elementos")
            if len(mediaUrls) > 0:
                print(f"   Primer elemento: {mediaUrls[0]}")
                print(f"   Todos los elementos: {mediaUrls}")
        elif isinstance(mediaUrls, dict):
            print(f"   Es un diccionario:")
            print(f"   {json.dumps(mediaUrls, indent=6, ensure_ascii=False)}")
        else:
            print(f"   Valor: {mediaUrls}")
        
        print(f"\n3. Buscando otros campos relacionados con imágenes:")
        for key in primer_item.keys():
            key_lower = key.lower()
            if any(word in key_lower for word in ['image', 'img', 'photo', 'picture', 'thumbnail', 'visual']):
                valor = primer_item[key]
                print(f"   {key}: {type(valor).__name__}")
                if isinstance(valor, str):
                    print(f"      Valor: {valor[:100]}")
                elif isinstance(valor, list) and len(valor) > 0:
                    print(f"      Lista con {len(valor)} elementos, primer elemento: {valor[0] if isinstance(valor[0], str) else type(valor[0]).__name__}")
                elif isinstance(valor, dict):
                    print(f"      Diccionario con claves: {list(valor.keys())[:5]}")
    
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()

