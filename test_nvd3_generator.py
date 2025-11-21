"""
Test para verificar la generación HTML con NVD3.js
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

print("=" * 60)
print("TEST GENERACIÓN HTML NVD3.JS")
print("=" * 60)

try:
    from smart_reports.utils.visualization.nvd3_generator import MotorTemplatesNVD3
    print("\n✅ MotorTemplatesNVD3 importado correctamente")
except ImportError as e:
    print(f"\n❌ Error importando generador: {e}")
    sys.exit(1)

# ============================================================
# TEST 1: Gráfico de Barras
# ============================================================
print("\n" + "=" * 60)
print("TEST 1: Gráfico de Barras NVD3")
print("=" * 60)

datos_barras = {
    'labels': ['Producto A', 'Producto B', 'Producto C', 'Producto D'],
    'values': [120, 250, 180, 320]
}

html_bar = MotorTemplatesNVD3.generar_grafico_barras(
    titulo="Ventas por Producto",
    datos=datos_barras,
    subtitulo="Gráfico de barras con NVD3.js",
    tema='dark'
)

print(f"✅ HTML generado: {len(html_bar)} caracteres\n")

# Verificaciones específicas de NVD3
checks_bar = {
    'D3.js v3 (requerido por NVD3)': 'd3/3.5.17/d3.min.js' in html_bar,
    'NVD3.js CDN': 'nvd3/1.8.6/nv.d3.min.js' in html_bar,
    'NVD3 CSS': 'nvd3/1.8.6/nv.d3.min.css' in html_bar,
    'Chart SVG container': '<svg id="chart"' in html_bar,
    'nv.addGraph': 'nv.addGraph' in html_bar,
    'discreteBarChart model': 'nv.models.discreteBarChart' in html_bar,
    'Datos JSON': '"x":' in html_bar and '"y":' in html_bar,
    'Tooltip customizado': '.tooltip.contentGenerator' in html_bar,
    'Formato números': "d3.format(',.0f')" in html_bar
}

print("Verificaciones Gráfico de Barras:")
print("-" * 60)
all_passed_bar = True
for check_name, result in checks_bar.items():
    status = "✅" if result else "❌"
    print(f"{status} {check_name}")
    if not result:
        all_passed_bar = False

# ============================================================
# TEST 2: Gráfico de Dona (Pie Chart)
# ============================================================
print("\n" + "=" * 60)
print("TEST 2: Gráfico de Dona NVD3")
print("=" * 60)

datos_donut = {
    'labels': ['Marketing', 'Ventas', 'IT', 'Operaciones'],
    'values': [30, 45, 15, 10]
}

html_donut = MotorTemplatesNVD3.generar_grafico_donut(
    titulo="Distribución de Presupuesto",
    datos=datos_donut,
    subtitulo="Gráfico de dona con NVD3.js",
    tema='dark'
)

print(f"✅ HTML generado: {len(html_donut)} caracteres\n")

checks_donut = {
    'NVD3.js CDN': 'nvd3/1.8.6/nv.d3.min.js' in html_donut,
    'pieChart model': 'nv.models.pieChart' in html_donut,
    'Modo donut': '.donut(true)' in html_donut,
    'Ratio donut': '.donutRatio(0.35)' in html_donut,
    'Etiquetas porcentaje': 'labelType("percent")' in html_donut,
    'Datos con label/value': '"label":' in html_donut and '"value":' in html_donut
}

print("Verificaciones Gráfico de Dona:")
print("-" * 60)
all_passed_donut = True
for check_name, result in checks_donut.items():
    status = "✅" if result else "❌"
    print(f"{status} {check_name}")
    if not result:
        all_passed_donut = False

# ============================================================
# TEST 3: Gráfico de Líneas
# ============================================================
print("\n" + "=" * 60)
print("TEST 3: Gráfico de Líneas NVD3")
print("=" * 60)

datos_linea = {
    'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    'values': [65, 72, 78, 85, 92, 88]
}

html_line = MotorTemplatesNVD3.generar_grafico_lineas(
    titulo="Tendencia Mensual",
    datos=datos_linea,
    subtitulo="Gráfico de líneas con NVD3.js",
    tema='dark'
)

print(f"✅ HTML generado: {len(html_line)} caracteres\n")

checks_line = {
    'lineChart model': 'nv.models.lineChart' in html_line,
    'useInteractiveGuideline': 'useInteractiveGuideline: true' in html_line,
    'Formato eje X con labels': 'labels[d]' in html_line,
    'Serie con key/values': '"key":' in html_line and '"values":' in html_line
}

print("Verificaciones Gráfico de Líneas:")
print("-" * 60)
all_passed_line = True
for check_name, result in checks_line.items():
    status = "✅" if result else "❌"
    print(f"{status} {check_name}")
    if not result:
        all_passed_line = False

# ============================================================
# TEST 4: Gráfico de Área
# ============================================================
print("\n" + "=" * 60)
print("TEST 4: Gráfico de Área Apilada NVD3")
print("=" * 60)

datos_area = {
    'labels': ['Ene', 'Feb', 'Mar', 'Abr'],
    'values': [100, 150, 120, 180]
}

html_area = MotorTemplatesNVD3.generar_grafico_area(
    titulo="Área de Ventas",
    datos=datos_area,
    subtitulo="Gráfico de área con NVD3.js",
    tema='dark'
)

print(f"✅ HTML generado: {len(html_area)} caracteres\n")

checks_area = {
    'stackedAreaChart model': 'nv.models.stackedAreaChart' in html_area,
    'Botones de estilo': 'chart.style(' in html_area,
    'Modo stack': "chart.style('stack')" in html_area,
    'Modo stream': "chart.style('stream')" in html_area,
    'Modo expand': "chart.style('expand')" in html_area,
    'clipEdge': '.clipEdge(true)' in html_area
}

print("Verificaciones Gráfico de Área:")
print("-" * 60)
all_passed_area = True
for check_name, result in checks_area.items():
    status = "✅" if result else "❌"
    print(f"{status} {check_name}")
    if not result:
        all_passed_area = False

# ============================================================
# RESUMEN FINAL
# ============================================================
print("\n" + "=" * 60)
print("RESUMEN FINAL")
print("=" * 60)

all_tests_passed = all_passed_bar and all_passed_donut and all_passed_line and all_passed_area

if all_tests_passed:
    print("✅ TODOS LOS TESTS PASARON")
    print("\n📊 Generador NVD3.js funcionando correctamente")
    print("💡 NVD3.js usa D3.js v3 y proporciona componentes reutilizables")
else:
    print("⚠️ ALGUNOS TESTS FALLARON")

print("\n🔧 Diferencias clave D3.js vs NVD3.js:")
print("-" * 60)
print("• D3.js: Máxima flexibilidad, control total, código personalizado")
print("• NVD3.js: Componentes pre-construidos, menos código, más rápido")
print("• NVD3 usa D3 v3.5.17 (estable pero más antigua)")
print("• D3 puro permite usar D3 v7 (más moderno)")

print("\n" + "=" * 60)
print("TEST COMPLETADO")
print("=" * 60)
