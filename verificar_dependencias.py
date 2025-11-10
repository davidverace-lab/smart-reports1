"""
Script de verificación de dependencias
Ejecuta ANTES de python main.py
"""
import sys

print("=" * 60)
print("🔍 VERIFICANDO DEPENDENCIAS - Smart Reports")
print("=" * 60)

errors = []
warnings = []

# Verificar Python version
print(f"\n✓ Python {sys.version.split()[0]}")

# Dependencias críticas
critical_deps = {
    'customtkinter': 'UI moderna',
    'pandas': 'Procesamiento de datos',
    'openpyxl': 'Excel',
    'reportlab': 'PDFs',
}

# Dependencias de base de datos
db_deps = {
    'pyodbc': 'SQL Server',
    'mysql.connector': 'MySQL',
}

# Dependencias de visualización
viz_deps = {
    'tkinterweb': 'D3.js interactivo',
    'matplotlib': 'Gráficos estáticos',
}

def check_module(module_name, description):
    """Verificar si un módulo está instalado"""
    try:
        if module_name == 'mysql.connector':
            import mysql.connector
        else:
            __import__(module_name)
        return True, None
    except ImportError as e:
        return False, str(e)

# Verificar dependencias críticas
print("\n📦 DEPENDENCIAS CRÍTICAS:")
for module, desc in critical_deps.items():
    success, error = check_module(module, desc)
    if success:
        print(f"  ✓ {module:20s} - {desc}")
    else:
        print(f"  ❌ {module:20s} - {desc} (FALTA)")
        errors.append(f"{module} ({desc})")

# Verificar dependencias de base de datos
print("\n💾 BASES DE DATOS:")
db_available = []
for module, desc in db_deps.items():
    success, error = check_module(module, desc)
    if success:
        print(f"  ✓ {module:20s} - {desc}")
        db_available.append(desc)
    else:
        print(f"  ⚠️  {module:20s} - {desc} (opcional)")
        warnings.append(f"{module} ({desc})")

if not db_available:
    print("\n  ⚠️  ADVERTENCIA: No hay drivers de BD instalados")
    print("     Instala al menos uno:")
    print("       - pip install pyodbc (SQL Server)")
    print("       - pip install mysql-connector-python (MySQL)")

# Verificar visualización
print("\n📊 VISUALIZACIÓN D3.js:")
for module, desc in viz_deps.items():
    success, error = check_module(module, desc)
    if success:
        print(f"  ✓ {module:20s} - {desc}")
    else:
        print(f"  ⚠️  {module:20s} - {desc} (recomendado)")
        warnings.append(f"{module} ({desc})")

# Resultado final
print("\n" + "=" * 60)
if errors:
    print("❌ FALTAN DEPENDENCIAS CRÍTICAS:")
    for err in errors:
        print(f"   - {err}")
    print("\n💡 SOLUCIÓN:")
    print("   pip install -r requirements.txt")
    print("=" * 60)
    sys.exit(1)
elif warnings:
    print("⚠️  DEPENDENCIAS OPCIONALES FALTANTES:")
    for warn in warnings:
        print(f"   - {warn}")
    print("\n💡 Recomendación: pip install -r requirements.txt")
    print("=" * 60)
    print("✅ Puedes continuar, pero algunas funciones estarán limitadas")
else:
    print("✅ TODAS LAS DEPENDENCIAS INSTALADAS")
    print("=" * 60)
    print("🚀 Todo listo para ejecutar: python main.py")

print()
