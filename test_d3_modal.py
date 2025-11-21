"""
Script de prueba para verificar que el modal D3.js funciona correctamente
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

print("=" * 60)
print("TEST MODAL D3.JS - VERIFICACIÓN")
print("=" * 60)

# 1. Verificar importación de tkinterweb
print("\n1️⃣  Verificando tkinterweb...")
try:
    from tkinterweb import HtmlFrame
    print("   ✅ tkinterweb instalado correctamente")
    TKINTERWEB_AVAILABLE = True
except ImportError as e:
    print(f"   ❌ tkinterweb NO disponible: {e}")
    print("   💡 Instala con: pip install tkinterweb>=3.23.0")
    TKINTERWEB_AVAILABLE = False

# 2. Verificar modal D3.js
print("\n2️⃣  Verificando modal D3.js...")
try:
    from smart_reports.ui.components.charts.modal_d3_fullscreen import ModalD3Fullscreen, TKINTERWEB_AVAILABLE as MODAL_TKINTERWEB
    print("   ✅ modal_d3_fullscreen importado correctamente")
    print(f"   ℹ️  TKINTERWEB_AVAILABLE en modal: {MODAL_TKINTERWEB}")
except ImportError as e:
    print(f"   ❌ Error importando modal: {e}")
    sys.exit(1)

# 3. Verificar generador D3.js
print("\n3️⃣  Verificando generador D3.js...")
try:
    from smart_reports.utils.visualization.d3_generator import MotorTemplatesD3
    print("   ✅ MotorTemplatesD3 importado correctamente")
except ImportError as e:
    print(f"   ❌ Error importando generador: {e}")
    sys.exit(1)

# 4. Probar generación de HTML
print("\n4️⃣  Probando generación de HTML...")
try:
    datos_prueba = {
        'labels': ['A', 'B', 'C', 'D', 'E'],
        'values': [10, 25, 15, 30, 20]
    }

    html = MotorTemplatesD3.generar_grafico_barras(
        titulo="Gráfico de Prueba",
        datos=datos_prueba,
        subtitulo="Prueba de generación D3.js",
        tema='dark',
        interactivo=True
    )

    print(f"   ✅ HTML generado correctamente ({len(html)} caracteres)")

    # Verificar que contiene elementos clave
    checks = {
        'D3.js CDN': 'd3.v7.min.js' in html,
        'Chart container': 'chart-container' in html,
        'Datos JSON': '"labels"' in html and '"values"' in html,
        'Script D3': 'const data' in html,
        'Botones': 'sortAscending' in html
    }

    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"      {status} {check_name}")

except Exception as e:
    print(f"   ❌ Error generando HTML: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. Probar modal interactivo (solo si tkinterweb disponible)
if TKINTERWEB_AVAILABLE and MODAL_TKINTERWEB:
    print("\n5️⃣  Probando modal interactivo...")
    print("   ℹ️  Abriendo ventana de prueba...")

    try:
        import customtkinter as ctk

        # Crear ventana principal
        root = ctk.CTk()
        root.title("Test Modal D3.js")
        root.geometry("800x600")

        # Configurar tema
        from smart_reports.config.gestor_temas import get_theme_manager
        theme_manager = get_theme_manager()
        theme_manager.set_theme('dark')

        # Frame principal
        frame = ctk.CTkFrame(root)
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            frame,
            text="Test Modal D3.js",
            font=('Montserrat', 24, 'bold')
        ).pack(pady=20)

        # Instrucciones
        ctk.CTkLabel(
            frame,
            text="Haz clic en los botones para probar los diferentes tipos de gráficos D3.js",
            font=('Montserrat', 12)
        ).pack(pady=10)

        # Datos de prueba
        datos_barras = {
            'labels': ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E'],
            'values': [120, 250, 180, 320, 200]
        }

        datos_donut = {
            'labels': ['Ventas', 'Marketing', 'Operaciones', 'IT', 'RRHH'],
            'values': [45, 25, 15, 10, 5]
        }

        datos_linea = {
            'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            'values': [65, 72, 78, 85, 92, 88]
        }

        # Funciones para abrir modales
        def open_bar_chart():
            modal = ModalD3Fullscreen(
                parent=root,
                title="Gráfico de Barras - Ventas por Producto",
                chart_type="bar",
                chart_data=datos_barras
            )
            modal.focus()
            modal.grab_set()

        def open_donut_chart():
            modal = ModalD3Fullscreen(
                parent=root,
                title="Gráfico de Dona - Distribución de Presupuesto",
                chart_type="donut",
                chart_data=datos_donut
            )
            modal.focus()
            modal.grab_set()

        def open_line_chart():
            modal = ModalD3Fullscreen(
                parent=root,
                title="Gráfico de Líneas - Tendencia Mensual",
                chart_type="line",
                chart_data=datos_linea
            )
            modal.focus()
            modal.grab_set()

        # Botones de prueba
        button_frame = ctk.CTkFrame(frame, fg_color='transparent')
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="📊 Gráfico de Barras",
            command=open_bar_chart,
            width=200,
            height=50,
            font=('Montserrat', 14, 'bold')
        ).pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="🍩 Gráfico de Dona",
            command=open_donut_chart,
            width=200,
            height=50,
            font=('Montserrat', 14, 'bold')
        ).pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="📈 Gráfico de Líneas",
            command=open_line_chart,
            width=200,
            height=50,
            font=('Montserrat', 14, 'bold')
        ).pack(pady=10)

        # Botón cerrar
        ctk.CTkButton(
            frame,
            text="Cerrar",
            command=root.destroy,
            width=150,
            height=40,
            fg_color='gray'
        ).pack(pady=20)

        print("   ✅ Ventana de prueba creada")
        print("   ℹ️  Prueba los botones para verificar el modal D3.js")

        root.mainloop()

    except Exception as e:
        print(f"   ❌ Error en prueba interactiva: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n5️⃣  Prueba interactiva omitida (tkinterweb no disponible)")

print("\n" + "=" * 60)
print("TEST COMPLETADO")
print("=" * 60)
