#!/usr/bin/env python
"""
Script para generar certificados SSL autofirmados para desarrollo
"""
import os
import subprocess
import sys
from pathlib import Path

def generate_certificates():
    """Genera certificados SSL autofirmados"""
    
    # Crear directorio de certificados
    cert_dir = Path('certs')
    cert_dir.mkdir(exist_ok=True)
    
    cert_file = cert_dir / 'cert.pem'
    key_file = cert_dir / 'key.pem'
    
    # Si ya existen certificados, preguntar si regenerar
    if cert_file.exists() and key_file.exists():
        response = input("Los certificados ya existen. ¿Deseas regenerarlos? (s/n): ").lower()
        if response != 's':
            print("Certificados mantienen sin cambios.")
            return
    
    print("Generando certificados SSL autofirmados...")
    print(f"Directorio: {cert_dir.absolute()}")
    
    try:
        # Generar certificado autofirmado válido por 365 días
        cmd = [
            'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
            '-keyout', str(key_file),
            '-out', str(cert_file),
            '-days', '365',
            '-nodes',
            '-subj', '/C=MX/ST=Mexico/L=Mexico/O=Ecommerce/CN=localhost'
        ]
        
        subprocess.run(cmd, check=True)
        
        print(f"✅ Certificado creado: {cert_file}")
        print(f"✅ Clave privada creada: {key_file}")
        print("\n⚠️  ADVERTENCIA: Estos certificados son solo para desarrollo.")
        print("   En producción, usa certificados de una autoridad certificadora confiable.")
        print("\nPuedes ejecutar la aplicación con HTTPS usando:")
        print("  python app.py")
        
    except FileNotFoundError:
        print("❌ Error: 'openssl' no está instalado.")
        print("\nPara Windows, puedes:")
        print("  1. Instalar OpenSSL: https://slproweb.com/products/Win32OpenSSL.html")
        print("  2. O usar WSL (Windows Subsystem for Linux)")
        print("  3. O instalar Git Bash que incluye OpenSSL")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al generar certificados: {e}")
        sys.exit(1)

if __name__ == '__main__':
    generate_certificates()
