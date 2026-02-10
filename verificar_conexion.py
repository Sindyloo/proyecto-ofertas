#!/usr/bin/env python3
"""
Script para verificar la configuración de red y firewall
"""
import socket
import sys

def get_local_ip():
    """Obtiene la IP local de manera confiable"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Error obteniendo IP: {e}")
        return None

def verificar_puerto(ip, puerto):
    """Verifica si el puerto está abierto"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        resultado = sock.connect_ex((ip, puerto))
        sock.close()
        return resultado == 0
    except Exception as e:
        print(f"Error verificando puerto: {e}")
        return False

def main():
    print("="*60)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DE RED")
    print("="*60)
    
    # Obtener IP local
    local_ip = get_local_ip()
    if local_ip:
        print(f"✅ IP Local detectada: {local_ip}")
    else:
        print("❌ No se pudo detectar la IP local")
        return
    
    # Verificar puerto 5000
    print(f"\n🔍 Verificando puerto 5000...")
    if verificar_puerto(local_ip, 5000):
        print(f"✅ Puerto 5000 está ABIERTO en {local_ip}")
    else:
        print(f"⚠️  Puerto 5000 NO está accesible")
        print(f"   Esto es normal si el servidor Flask no está corriendo")
    
    print("\n" + "="*60)
    print("📋 INSTRUCCIONES:")
    print("="*60)
    print(f"1. Inicia el servidor Flask: python app.py")
    print(f"2. En tu celular, abre el navegador y ve a:")
    print(f"   http://{local_ip}:5000")
    print(f"3. Si no carga, verifica:")
    print(f"   - Que ambos dispositivos estén en la misma red WiFi")
    print(f"   - Que el firewall de Windows permita el puerto 5000")
    print(f"   - Que el servidor Flask esté corriendo")
    print("\n💡 Para abrir el firewall en Windows:")
    print("   - Abre PowerShell como Administrador")
    print("   - Ejecuta: New-NetFirewallRule -DisplayName 'Flask App' -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow")
    print("="*60)

if __name__ == "__main__":
    main()

