"""
Script de prueba simple para verificar la generación HTML D3.js
(Sin dependencias de GUI)
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

print("=" * 60)
print("TEST GENERACIÓN HTML D3.JS")
print("=" * 60)

try:
    from smart_reports.utils.visualization.d3_generator import MotorTemplatesD3
    print("\n✅ MotorTemplatesD3 importado correctamente")
except ImportError as e:
    print(f"\n❌ Error importando generador: {e}")
    sys.exit(1)

# Datos de prueba
datos_prueba = {
    'labels': ['A', 'B', 'C', 'D', 'E'],
    'values': [10, 25, 15, 30, 20]
}

# Generar HTML
print("\n📊 Generando gráfico de barras...")
html = MotorTemplatesD3.generar_grafico_barras(
    titulo="Gráfico de Prueba",
    datos=datos_prueba,
    subtitulo="Prueba de generación D3.js",
    tema='dark',
    interactivo=True
)

print(f"✅ HTML generado: {len(html)} caracteres\n")

# Verificaciones con los patrones CORREGIDOS
checks = {
    'D3.js CDN': 'd3.v7.min.js' in html,
    'Chart container': 'chart-container' in html,
    'Datos JSON (labels:)': 'labels:' in html,
    'Datos JSON (values:)': 'values:' in html,
    'Script D3 (const rawData)': 'const rawData' in html,
    'Script D3 (let data)': 'let data' in html,
    'Botones de interacción': 'sortAscending' in html,
    'Tooltip D3': 'd3-tooltip' in html,
    'Escalas D3': 'd3.scaleBand' in html,
    'Animaciones': 'transition()' in html
}

print("Verificaciones:")
print("-" * 60)
all_passed = True
for check_name, result in checks.items():
    status = "✅" if result else "❌"
    print(f"{status} {check_name}")
    if not result:
        all_passed = False

print("\n" + "=" * 60)
if all_passed:
    print("✅ TODAS LAS VERIFICACIONES PASARON")
else:
    print("⚠️ ALGUNAS VERIFICACIONES FALLARON")
print("=" * 60)

# Mostrar muestra del HTML generado
print("\nMuestra del HTML generado (primeros 500 caracteres):")
print("-" * 60)
print(html[:500])
print("...")
