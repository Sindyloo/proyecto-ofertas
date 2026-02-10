# Script para abrir el puerto 5000 en el firewall de Windows
# Ejecutar como Administrador

Write-Host "=" -NoNewline
Write-Host ("=" * 59)
Write-Host "🔥 CONFIGURANDO FIREWALL PARA FLASK"
Write-Host "=" -NoNewline
Write-Host ("=" * 59)

# Verificar si ya existe la regla
$reglaExistente = Get-NetFirewallRule -DisplayName "Flask App" -ErrorAction SilentlyContinue

if ($reglaExistente) {
    Write-Host "✅ La regla del firewall ya existe"
    Write-Host "   Eliminando regla anterior..."
    Remove-NetFirewallRule -DisplayName "Flask App" -ErrorAction SilentlyContinue
}

Write-Host "📝 Creando nueva regla del firewall..."
try {
    New-NetFirewallRule -DisplayName "Flask App" `
        -Direction Inbound `
        -LocalPort 5000 `
        -Protocol TCP `
        -Action Allow `
        -Description "Permite acceso al servidor Flask desde la red local"
    
    Write-Host "✅ Regla del firewall creada exitosamente"
    Write-Host ""
    Write-Host "🚀 Ahora puedes iniciar el servidor Flask:"
    Write-Host "   python app.py"
    Write-Host ""
    Write-Host "📱 Y acceder desde tu celular usando la IP que muestra el servidor"
} catch {
    Write-Host "❌ Error creando regla del firewall: $_"
    Write-Host ""
    Write-Host "💡 Asegúrate de ejecutar este script como Administrador"
    Write-Host "   Click derecho en PowerShell -> Ejecutar como administrador"
}

Write-Host "=" -NoNewline
Write-Host ("=" * 59)

