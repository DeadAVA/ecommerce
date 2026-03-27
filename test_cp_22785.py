#!/usr/bin/env python3
"""
Script para verificar si CP 22785 existe en el XML
"""
import re
import os

xml_path = 'api_zonas/data/CPdescarga.xml'

print(f"Buscando CP 22785 en {xml_path}...")
print()

# Leer el archivo
with open(xml_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Buscar todas las ocurrencias de 22785
matches = re.findall(r'.*22785.*', content)
print(f"Encontradas {len(matches)} líneas con '22785'")

if matches:
    for i, match in enumerate(matches[:5]):
        print(f"\n[{i+1}] {match[:200]}")

# Ahora parsear los records que contienen 22785
print("\n" + "="*80)
print("Parseando registros con CP 22785...")
print("="*80)

table_pattern = r'<table[^>]*>(.*?)</table>'
tables = re.findall(table_pattern, content, re.DOTALL)

found_records = []
for table_content in tables:
    # Buscar d_CP
    cp_match = re.search(r'<d_CP[^>]*>([^<]+)</d_CP>', table_content)
    if cp_match and cp_match.group(1).strip() == '22785':
        # Parsear todo el record
        element_pattern = r'<([^/>]+)>([^<]*)</\1>'
        matches = re.findall(element_pattern, table_content)
        record = {}
        for tag, value in matches:
            tag = tag.split()[0]
            record[tag] = value.strip()
        
        found_records.append(record)

print(f"\nEncontrados {len(found_records)} registros para CP 22785\n")

if found_records:
    for i, record in enumerate(found_records[:3]):
        print(f"\n--- Registro {i+1} ---")
        for key, value in sorted(record.items()):
            if value:
                print(f"  {key}: {value}")
else:
    print("❌ NO SE ENCONTRARON REGISTROS PARA CP 22785")
    print("\nProbando con otros CPs para verificar que el parser funciona...")
    
    # Buscar algunos CPs que existan
    cp_set = set()
    for table_content in tables:
        cp_match = re.search(r'<d_CP[^>]*>([^<]+)</d_CP>', table_content)
        if cp_match:
            cp = cp_match.group(1).strip()
            cp_set.add(cp)
            if len(cp_set) >= 5:
                break
    
    print(f"\nPrimeros CPs encontrados en el XML: {sorted(cp_set)}")
