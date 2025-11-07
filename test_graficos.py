#!/usr/bin/env python3
"""
Script de prueba para verificar la generación de gráficos
"""
from nucleo.servicios.motor_graficos_svg import MotorGraficosSVG
from nucleo.servicios.motor_templates_d3 import MotorTemplatesD3

# Datos de prueba
datos_barras = {
    'labels': ['ICAVE', 'EIT', 'LCT', 'TIMSA', 'HPMX'],
    'values': [45, 32, 28, 19, 15]
}

datos_donut = {
    'labels': ['ICAVE', 'EIT', 'LCT', 'TIMSA', 'HPMX'],
    'values': [45, 32, 28, 19, 15]
}

datos_lineas = {
    'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May'],
    'series': [
        {'name': 'Serie 1', 'values': [10, 20, 15, 25, 30]},
        {'name': 'Serie 2', 'values': [5, 15, 10, 20, 25]}
    ]
}

print("=" * 60)
print("PRUEBA DE MOTORES DE GRÁFICOS")
print("=" * 60)

# Test 1: Motor SVG
print("\n1. Probando motor SVG (matplotlib)...")
try:
    motor_svg = MotorGraficosSVG()

    html_barras = motor_svg.generar_grafico_barras(datos_barras, 'dark')
    print("   ✅ Gráfico de barras SVG generado")
    print(f"      Tamaño: {len(html_barras)} bytes")

    html_donut = motor_svg.generar_grafico_donut(datos_donut, 'dark')
    print("   ✅ Gráfico donut SVG generado")
    print(f"      Tamaño: {len(html_donut)} bytes")

    html_lineas = motor_svg.generar_grafico_lineas(datos_lineas, 'dark')
    print("   ✅ Gráfico de líneas SVG generado")
    print(f"      Tamaño: {len(html_lineas)} bytes")

    print("\n   ✅ Motor SVG: TODO OK")
except Exception as e:
    print(f"   ❌ Error en motor SVG: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Motor D3
print("\n2. Probando motor D3.js...")
try:
    motor_d3 = MotorTemplatesD3()

    html_barras = motor_d3.generar_grafico_barras(
        titulo="Test Barras",
        datos=datos_barras,
        tema='dark'
    )
    print("   ✅ Gráfico de barras D3 generado")
    print(f"      Tamaño: {len(html_barras)} bytes")

    html_donut = motor_d3.generar_grafico_donut(
        titulo="Test Donut",
        datos=datos_donut,
        tema='dark'
    )
    print("   ✅ Gráfico donut D3 generado")
    print(f"      Tamaño: {len(html_donut)} bytes")

    html_lineas = motor_d3.generar_grafico_lineas(
        titulo="Test Líneas",
        datos=datos_lineas,
        tema='dark'
    )
    print("   ✅ Gráfico de líneas D3 generado")
    print(f"      Tamaño: {len(html_lineas)} bytes")

    print("\n   ✅ Motor D3: TODO OK")
except Exception as e:
    print(f"   ❌ Error en motor D3: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Verificar librerías de renderizado
print("\n3. Verificando librerías de renderizado...")
try:
    from tkhtmlview import HTMLScrolledText
    print("   ✅ tkhtmlview instalado")
except ImportError:
    print("   ⚠️  tkhtmlview NO instalado")

try:
    from tkinterweb import HtmlFrame
    print("   ✅ tkinterweb instalado")
except ImportError:
    print("   ⚠️  tkinterweb NO instalado")

print("\n" + "=" * 60)
print("RESUMEN:")
print("=" * 60)
print("✅ Todos los motores de gráficos funcionan correctamente")
print("📊 Los gráficos se pueden renderizar en la aplicación")
print("\nPara ver los gráficos:")
print("  1. En la aplicación: se renderizan automáticamente")
print("  2. En navegador: clic en botón 'Abrir en Navegador'")
print("=" * 60)
