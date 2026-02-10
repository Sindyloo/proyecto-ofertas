#!/usr/bin/env python3
"""
Script para probar que el servidor Flask funciona correctamente
"""
import requests
import sys
import time

def probar_servidor(url_base="http://localhost:5000"):
    """Prueba los endpoints del servidor"""
    print("="*60)
    print("🧪 PROBANDO SERVIDOR FLASK")
    print("="*60)
    
    # Probar endpoint de prueba
    print("\n1. Probando endpoint /test...")
    try:
        response = requests.get(f"{url_base}/test", timeout=5)
        if response.status_code == 200:
            print("   ✅ Endpoint /test funciona correctamente")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"   ❌ Error: Status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ ERROR: No se puede conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   python app.py")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Probar endpoint principal
    print("\n2. Probando endpoint / (página principal)...")
    try:
        response = requests.get(f"{url_base}/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Página principal carga correctamente")
        else:
            print(f"   ⚠️  Status code: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    print("\n" + "="*60)
    print("✅ El servidor está funcionando correctamente")
    print("="*60)
    return True

if __name__ == "__main__":
    # Permitir especificar URL como argumento
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    probar_servidor(url)

