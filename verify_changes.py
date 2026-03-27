#!/usr/bin/env python
"""
Script de verificación post-actualización
Valida que todos los cambios se aplicaron correctamente
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Verifica si un archivo existe"""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {description}: {file_path} ({size} bytes)")
        return True
    else:
        print(f"❌ {description}: NO ENCONTRADO - {file_path}")
        return False

def check_content_in_file(file_path, content, description):
    """Verifica si contenido específico existe en un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            if content in file_content:
                print(f"✅ {description}: ENCONTRADO")
                return True
            else:
                print(f"❌ {description}: NO ENCONTRADO")
                return False
    except Exception as e:
        print(f"❌ {description}: Error leyendo archivo - {str(e)}")
        return False

def main():
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║   🔍 VERIFICACIÓN POST-ACTUALIZACIÓN                     ║")
    print("║   Ecommerce - Seguridad y HTTPS                           ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    results = []
    
    # Verificar archivos nuevos
    print("📁 ARCHIVOS NUEVOS:")
    print("─" * 60)
    results.append(check_file_exists("generate_certs.py", "generate_certs.py"))
    results.append(check_file_exists("HTTPS_SETUP.md", "HTTPS_SETUP.md"))
    results.append(check_file_exists("CAMBIOS_REALIZADOS.md", "CAMBIOS_REALIZADOS.md"))
    results.append(check_file_exists(".env.example", ".env.example"))
    results.append(check_file_exists("setup.ps1", "setup.ps1"))
    results.append(check_file_exists("README_ARREGLOS.md", "README_ARREGLOS.md"))
    results.append(check_file_exists("INICIO_RAPIDO.txt", "INICIO_RAPIDO.txt"))
    
    # Verificar cambios en app.py
    print("\n📝 CAMBIOS EN app.py:")
    print("─" * 60)
    results.append(check_content_in_file("app.py", "import os", "Import de os"))
    results.append(check_content_in_file("app.py", "import ssl", "Import de ssl"))
    results.append(check_content_in_file("app.py", "import logging", "Import de logging"))
    results.append(check_content_in_file("app.py", "logger = logging.getLogger", "Logger configurado"))
    results.append(check_content_in_file("app.py", "Strict-Transport-Security", "Header HSTS"))
    results.append(check_content_in_file("app.py", "Content-Security-Policy", "Header CSP"))
    results.append(check_content_in_file("app.py", "SESSION_COOKIE_SECURE", "Cookie segura configurada"))
    results.append(check_content_in_file("app.py", "ssl.SSLContext", "SSL Context configurado"))
    
    # Verificar cambios en config.py
    print("\n⚙️  CAMBIOS EN config.py:")
    print("─" * 60)
    results.append(check_content_in_file("config.py", "PREFERRED_URL_SCHEME", "HTTPS scheme preferido"))
    results.append(check_content_in_file("config.py", "SESSION_COOKIE_SECURE", "Cookies seguras"))
    results.append(check_content_in_file("config.py", "SESSION_COOKIE_HTTPONLY", "Cookies HttpOnly"))
    results.append(check_content_in_file("config.py", "os.environ.get", "Variables de entorno"))
    
    # Verificar validaciones
    print("\n🛡️  VALIDACIONES MEJORADAS:")
    print("─" * 60)
    results.append(check_content_in_file("app.py", "try:\n        username = request.form.get", "Validación en register"))
    results.append(check_content_in_file("app.py", "if producto.stock <= 0:", "Validación de stock en carrito"))
    results.append(check_content_in_file("app.py", "if new_quantity < 1:", "Validación de cantidad"))
    results.append(check_content_in_file("app.py", "for item in carrito_items:", "Loop de items mejorado"))
    
    # Verificar manejo de errores
    print("\n⚠️  MANEJO DE ERRORES:")
    print("─" * 60)
    results.append(check_content_in_file("app.py", "except Exception as e:", "Try-catch implementado"))
    results.append(check_content_in_file("app.py", "db.session.rollback()", "Rollback en errores"))
    results.append(check_content_in_file("app.py", "logger.error", "Logging de errores"))
    results.append(check_content_in_file("app.py", "logger.info", "Logging de info"))
    
    # Resumen
    print("\n╔═══════════════════════════════════════════════════════════╗")
    total = len(results)
    passed = sum(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    if percentage == 100:
        print(f"║ ✅ VERIFICACIÓN COMPLETADA: {passed}/{total} (100%)     ║")
        print("║ Todos los cambios se aplicaron correctamente           ║")
    elif percentage >= 80:
        print(f"║ ⚠️  VERIFICACIÓN PARCIAL: {passed}/{total} ({percentage:.0f}%)        ║")
        print("║ La mayoría de cambios se aplicaron                    ║")
    else:
        print(f"║ ❌ VERIFICACIÓN FALLIDA: {passed}/{total} ({percentage:.0f}%)         ║")
        print("║ Revisa los errores arriba                             ║")
    
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    # Instrucciones finales
    print("📋 PRÓXIMOS PASOS:")
    print("─" * 60)
    if percentage == 100:
        print("1. Copia .env.example a .env: copy .env.example .env")
        print("2. Edita .env con tus valores de configuración")
        print("3. Genera certificados SSL: python generate_certs.py")
        print("4. Instala dependencias: pip install -r requirements.txt")
        print("5. Ejecuta la app: python app.py")
        print("6. Accede a: https://localhost")
    else:
        print("❌ Revisa los errores en la verificación")
        print("   y asegúrate de que se aplicaron todos los cambios")
    
    print("\n📚 DOCUMENTACIÓN:")
    print("─" * 60)
    print("• INICIO_RAPIDO.txt - Guía paso a paso")
    print("• HTTPS_SETUP.md - Documentación detallada de HTTPS")
    print("• CAMBIOS_REALIZADOS.md - Detalle técnico de cambios")
    print("• README_ARREGLOS.md - Resumen ejecutivo")
    print()
    
    return 0 if percentage == 100 else 1

if __name__ == '__main__':
    sys.exit(main())
