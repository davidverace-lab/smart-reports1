"""
Ejemplo de Dashboard con gráficos NVD3.js integrados
Demuestra el uso de InteractiveChartCard con motor NVD3
"""
import customtkinter as ctk
from smart_reports.ui.components.charts.interactive_chart_card import InteractiveChartCard
from smart_reports.config.gestor_temas import get_theme_manager

# Crear ventana principal
root = ctk.CTk()
root.title("Dashboard con NVD3.js - Smart Reports")
root.geometry("1400x900")

# Configurar tema
theme_manager = get_theme_manager()
theme_manager.set_theme('dark')

# Contenedor principal con scroll
main_container = ctk.CTkScrollableFrame(root)
main_container.pack(fill='both', expand=True, padx=20, pady=20)

# Título del dashboard
ctk.CTkLabel(
    main_container,
    text="📊 Dashboard Interactivo - NVD3.js",
    font=('Montserrat', 32, 'bold')
).pack(pady=(0, 20))

# Descripción
desc_frame = ctk.CTkFrame(main_container, fg_color='#1a4d7a')
desc_frame.pack(fill='x', pady=(0, 30))

ctk.CTkLabel(
    desc_frame,
    text="Gráficos con motor NVD3.js - Haz clic en ↗ para ver en fullscreen interactivo",
    font=('Montserrat', 14),
    text_color='white'
).pack(pady=15)

# ============================================================
# FILA 1: Barras y Dona
# ============================================================
row1 = ctk.CTkFrame(main_container, fg_color='transparent')
row1.pack(fill='x', pady=10)

# Gráfico de Barras (NVD3)
chart1_frame = ctk.CTkFrame(row1, fg_color='transparent')
chart1_frame.pack(side='left', fill='both', expand=True, padx=5)

chart1 = InteractiveChartCard(
    chart1_frame,
    title='Ventas Mensuales 2025',
    width=650,
    height=400,
    chart_engine='nvd3'  # ← Motor NVD3.js
)
chart1.pack(fill='both', expand=True)

# Datos ejemplo
datos_ventas = {
    'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    'values': [1200, 1850, 1450, 2200, 1900, 2400]
}
chart1.set_chart('bar', datos_ventas)

# Gráfico de Dona (NVD3)
chart2_frame = ctk.CTkFrame(row1, fg_color='transparent')
chart2_frame.pack(side='left', fill='both', expand=True, padx=5)

chart2 = InteractiveChartCard(
    chart2_frame,
    title='Distribución por Producto',
    width=650,
    height=400,
    chart_engine='nvd3'  # ← Motor NVD3.js
)
chart2.pack(fill='both', expand=True)

datos_productos = {
    'labels': ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E'],
    'values': [35, 25, 20, 12, 8]
}
chart2.set_chart('donut', datos_productos)

# ============================================================
# FILA 2: Líneas
# ============================================================
row2 = ctk.CTkFrame(main_container, fg_color='transparent')
row2.pack(fill='x', pady=10)

chart3_frame = ctk.CTkFrame(row2, fg_color='transparent')
chart3_frame.pack(fill='both', expand=True, padx=5)

chart3 = InteractiveChartCard(
    chart3_frame,
    title='Tendencia de Crecimiento - Comparativa',
    width=1300,
    height=450,
    chart_engine='nvd3'  # ← Motor NVD3.js
)
chart3.pack(fill='both', expand=True)

# Datos con múltiples series
datos_tendencia = {
    'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago'],
    'series': [
        {
            'name': 'Ventas 2024',
            'values': [1000, 1200, 1100, 1400, 1300, 1600, 1500, 1800]
        },
        {
            'name': 'Ventas 2025',
            'values': [1200, 1500, 1400, 1800, 1700, 2100, 2000, 2400]
        }
    ]
}
chart3.set_chart('line', datos_tendencia)

# ============================================================
# COMPARACIÓN: D3.js vs NVD3.js
# ============================================================
row3 = ctk.CTkFrame(main_container, fg_color='transparent')
row3.pack(fill='x', pady=20)

# Título comparación
ctk.CTkLabel(
    row3,
    text="🔬 Comparación: D3.js vs NVD3.js (mismo gráfico, diferente motor)",
    font=('Montserrat', 18, 'bold')
).pack(pady=10)

comparison_container = ctk.CTkFrame(row3, fg_color='transparent')
comparison_container.pack(fill='x')

# Gráfico con D3.js puro
d3_frame = ctk.CTkFrame(comparison_container, fg_color='transparent')
d3_frame.pack(side='left', fill='both', expand=True, padx=5)

chart_d3 = InteractiveChartCard(
    d3_frame,
    title='🟣 D3.js Puro (Máxima Personalización)',
    width=650,
    height=400,
    chart_engine='d3'  # ← Motor D3.js puro
)
chart_d3.pack(fill='both', expand=True)

datos_comparacion = {
    'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
    'values': [2500, 3200, 2900, 3800]
}
chart_d3.set_chart('bar', datos_comparacion)

# Gráfico con NVD3.js
nvd3_frame = ctk.CTkFrame(comparison_container, fg_color='transparent')
nvd3_frame.pack(side='left', fill='both', expand=True, padx=5)

chart_nvd3 = InteractiveChartCard(
    nvd3_frame,
    title='🔵 NVD3.js (Componentes Reutilizables)',
    width=650,
    height=400,
    chart_engine='nvd3'  # ← Motor NVD3.js
)
chart_nvd3.pack(fill='both', expand=True)

chart_nvd3.set_chart('bar', datos_comparacion)

# Nota explicativa
note_frame = ctk.CTkFrame(main_container, fg_color='#2a3a2a')
note_frame.pack(fill='x', pady=20)

note_text = """
💡 DIFERENCIAS:

• NVD3.js (Azul) - Default recomendado:
  ✅ Componentes pre-construidos → Desarrollo rápido
  ✅ HTML más ligero (~5 KB)
  ✅ Tooltips avanzados out-of-the-box
  ✅ Ideal para dashboards empresariales

• D3.js Puro (Morado) - Para casos especiales:
  ⭐ Control total sobre cada elemento
  ⭐ Animaciones personalizadas
  ⭐ D3.js v7 (última versión)
  ⭐ Ideal para visualizaciones únicas

👆 Haz clic en el botón ↗ de cualquier gráfico para ver en fullscreen interactivo
"""

ctk.CTkLabel(
    note_frame,
    text=note_text,
    font=('Montserrat', 12),
    justify='left',
    text_color='#90EE90'
).pack(pady=15, padx=20)

# Botón cerrar
ctk.CTkButton(
    main_container,
    text="Cerrar Dashboard",
    command=root.destroy,
    width=200,
    height=45,
    font=('Montserrat', 14, 'bold'),
    fg_color='gray'
).pack(pady=20)

print("""
╔════════════════════════════════════════════════════════════╗
║  DASHBOARD CON NVD3.JS - INSTRUCCIONES                    ║
╚════════════════════════════════════════════════════════════╝

1. Observa los gráficos Matplotlib estáticos en el dashboard
2. Haz clic en el botón ↗ (fullscreen) de cualquier gráfico
3. Se abrirá un modal con el gráfico interactivo NVD3.js
4. En el modal puedes:
   • Pasar el mouse para ver tooltips detallados
   • Hacer zoom y pan (según el tipo de gráfico)
   • Ordenar datos (en gráficos de barras)
   • Presionar ESC para cerrar

🔵 NVD3.js es el motor DEFAULT - rápido y confiable
🟣 D3.js puro disponible para casos especiales (usa engine='d3')

📖 Documentación: docs/D3_VS_NVD3.md
""")

root.mainloop()
