#!/bin/bash
# setup.sh - Script de configuración rápida para Windows PowerShell

Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Configuración Rápida - Ecommerce HTTPS Setup    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# 1. Crear archivo .env
Write-Host "`n📋 Creando archivo .env..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Archivo .env creado. Edítalo con tus valores." -ForegroundColor Green
} else {
    Write-Host "⚠️  El archivo .env ya existe." -ForegroundColor Yellow
}

# 2. Instalar dependencias
Write-Host "`n📦 Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencias instaladas correctamente." -ForegroundColor Green
} else {
    Write-Host "❌ Error al instalar dependencias." -ForegroundColor Red
    exit 1
}

# 3. Generar certificados SSL
Write-Host "`n🔐 Generando certificados SSL..." -ForegroundColor Yellow
python generate_certs.py

# 4. Mostrar instrucciones finales
Write-Host "`n╔════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║         ✅ CONFIGURACIÓN COMPLETADA ✅             ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n📝 Próximos Pasos:" -ForegroundColor Cyan
Write-Host "1️⃣  Edita el archivo .env con tus valores:" -ForegroundColor White
Write-Host "   - SECRET_KEY" -ForegroundColor Gray
Write-Host "   - DATABASE_URI" -ForegroundColor Gray
Write-Host "   - MAIL_USERNAME y MAIL_PASSWORD" -ForegroundColor Gray
Write-Host "   - POSTAL_NINJA_API_KEY" -ForegroundColor Gray

Write-Host "`n2️⃣  Inicia la aplicación:" -ForegroundColor White
Write-Host "   python app.py" -ForegroundColor Gray

Write-Host "`n3️⃣  Accede a:" -ForegroundColor White
Write-Host "   🔒 https://localhost (HTTPS)" -ForegroundColor Gray
Write-Host "   ⚠️  Ignora el warning del navegador sobre certificado autofirmado" -ForegroundColor Yellow

Write-Host "`n📚 Documentación:" -ForegroundColor Cyan
Write-Host "   - HTTPS_SETUP.md: Guía completa de HTTPS" -ForegroundColor Gray
Write-Host "   - CAMBIOS_REALIZADOS.md: Detalle de todos los arreglos" -ForegroundColor Gray

Write-Host "`n💡 Tips:" -ForegroundColor Cyan
Write-Host "   - Para desarrollo sin HTTPS: python app.py (HTTP)" -ForegroundColor Gray
Write-Host "   - Para regenerar certificados: python generate_certs.py" -ForegroundColor Gray
Write-Host "   - Usa variables de entorno en .env para credenciales" -ForegroundColor Gray

Write-Host "`n"
