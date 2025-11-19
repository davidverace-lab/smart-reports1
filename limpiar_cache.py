"""
Script de limpieza - Elimina archivos .pyc y __pycache__ antiguos
Ejecutar ANTES de iniciar la aplicación
"""
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

print("="*80)
print("LIMPIEZA DE ARCHIVOS CACHE DE PYTHON")
print("="*80)

# Contador
pycache_eliminados = 0
pyc_eliminados = 0

# Eliminar __pycache__
print("\n[1] Eliminando carpetas __pycache__...")
for root, dirs, files in os.walk(BASE_DIR):
    if '__pycache__' in dirs:
        pycache_path = os.path.join(root, '__pycache__')
        try:
            shutil.rmtree(pycache_path)
            pycache_eliminados += 1
            print(f"  ✓ Eliminado: {pycache_path}")
        except Exception as e:
            print(f"  ✗ Error eliminando {pycache_path}: {e}")

# Eliminar archivos .pyc
print("\n[2] Eliminando archivos .pyc...")
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith('.pyc'):
            pyc_path = os.path.join(root, file)
            try:
                os.remove(pyc_path)
                pyc_eliminados += 1
                print(f"  ✓ Eliminado: {pyc_path}")
            except Exception as e:
                print(f"  ✗ Error eliminando {pyc_path}: {e}")

print("\n" + "="*80)
print("RESUMEN")
print("="*80)
print(f"Carpetas __pycache__ eliminadas: {pycache_eliminados}")
print(f"Archivos .pyc eliminados: {pyc_eliminados}")
print("="*80)
print("\n✅ Limpieza completada")
print("\nAhora ejecuta:")
print("  python main.py")
print("="*80)
