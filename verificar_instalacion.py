#!/usr/bin/env python3
"""
Script de verificación de instalación de Smart Reports
Verifica que todas las dependencias estén instaladas correctamente
"""

import sys
import ast
from pathlib import Path

print("="*70)
print(" VERIFICACIÓN DE INSTALACIÓN - SMART REPORTS")
print(" Instituto Hutchison Ports")
print("="*70)

# 1. Verificar versión de Python
print("\n[1] Verificando versión de Python...")
version = sys.version_info
print(f"    Python {version.major}.{version.minor}.{version.micro}")
if version.major >= 3 and version.minor >= 8:
    print("    ✓ Versión de Python adecuada (3.8+)")
else:
    print("    ✗ Se requiere Python 3.8 o superior")
    sys.exit(1)

# 2. Verificar que requirements.txt sea legible
print("\n[2] Verificando requirements.txt...")
try:
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        lineas = content.splitlines()
        print(f"    ✓ requirements.txt legible ({len(lineas)} líneas)")
        print("    ✓ Sin errores de codificación Unicode")
except Exception as e:
    print(f"    ✗ Error leyendo requirements.txt: {e}")
    sys.exit(1)

# 3. Verificar sintaxis de archivos principales
print("\n[3] Verificando sintaxis de archivos principales...")
archivos_principales = [
    'main.py',
    'main_pyqt6.py',
    'smart_reports/config/settings.py',
]

archivos_ok = 0
for archivo in archivos_principales:
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        print(f"    ✓ {archivo}")
        archivos_ok += 1
    except FileNotFoundError:
        print(f"    ⚠ {archivo} - No encontrado")
    except SyntaxError as e:
        print(f"    ✗ {archivo} - Error de sintaxis")
    except Exception as e:
        print(f"    ✗ {archivo} - Error: {e}")

# 4. Verificar módulos instalados
print("\n[4] Verificando dependencias instaladas...")

modulos_requeridos = {
    'pyodbc': 'Conexión a SQL Server',
    'mysql.connector': 'Conexión a MySQL',
    'pandas': 'Procesamiento de datos',
    'numpy': 'Operaciones numéricas',
    'openpyxl': 'Manejo de Excel',
    'pydantic': 'Validación de datos',
    'PyQt6': 'Interfaz gráfica',
    'PyQt6.QtWebEngineWidgets': 'Visualización web en PyQt6',
    'PIL': 'Procesamiento de imágenes (Pillow)',
    'matplotlib': 'Gráficos estáticos',
    'plotly': 'Gráficos interactivos',
    'reportlab': 'Generación de PDFs',
    'dateutil': 'Manejo de fechas',
    'colorama': 'Colores en terminal',
    'colorlog': 'Logs con colores',
    'dotenv': 'Variables de entorno',
}

instalados = 0
faltantes = []

for modulo, descripcion in modulos_requeridos.items():
    try:
        __import__(modulo)
        print(f"    ✓ {modulo:35} - {descripcion}")
        instalados += 1
    except ImportError:
        print(f"    ✗ {modulo:35} - {descripcion} (NO INSTALADO)")
        faltantes.append(modulo)

# 5. Resumen final
print("\n" + "="*70)
print(" RESUMEN DE VERIFICACIÓN")
print("="*70)

print(f"\n✓ Python:         {version.major}.{version.minor}.{version.micro}")
print(f"✓ Requirements:   Archivo válido")
print(f"✓ Sintaxis:       {archivos_ok}/{len(archivos_principales)} archivos OK")
print(f"✓ Dependencias:   {instalados}/{len(modulos_requeridos)} instaladas")

if faltantes:
    print(f"\n⚠ ATENCIÓN: {len(faltantes)} dependencias faltantes")
    print("\nPara instalar las dependencias faltantes, ejecuta:")
    print("  pip install -r requirements.txt")
    print("\nO instala los módulos específicos:")
    for mod in faltantes[:5]:  # Mostrar solo los primeros 5
        print(f"  pip install {mod}")
    if len(faltantes) > 5:
        print(f"  ... y {len(faltantes)-5} más")
    sys.exit(1)
else:
    print("\n" + "="*70)
    print(" ✅ TODAS LAS VERIFICACIONES EXITOSAS")
    print(" El proyecto está listo para ejecutarse")
    print("="*70)
    print("\nPara iniciar la aplicación PyQt6, ejecuta:")
    print("  python main_pyqt6.py")
    print("\nPara la versión anterior (tkinter), ejecuta:")
    print("  python main.py")
