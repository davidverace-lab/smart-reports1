"""
Ejemplo simple para probar expansión in-place de gráficos D3/NVD3
NO abre ventanas modales - Se expande en el mismo lugar
"""
import customtkinter as ctk
from smart_reports.ui.components.charts.interactive_chart_card import InteractiveChartCard
from smart_reports.config.gestor_temas import get_theme_manager

# Crear ventana principal
root = ctk.CTk()
root.title("Test Expansión In-Place - NVD3.js")
root.geometry("1200x800")

# Configurar tema
theme_manager = get_theme_manager()
theme_manager.set_theme('dark')

# Frame principal
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill='both', expand=True, padx=30, pady=30)

# Título
ctk.CTkLabel(
    main_frame,
    text="🎨 Test: Expansión In-Place",
    font=('Montserrat', 28, 'bold')
).pack(pady=(0, 10))

# Instrucciones
instrucciones = """
📖 INSTRUCCIONES:

1. Observa el gráfico estático de Matplotlib abajo
2. Haz clic en el botón ↗ para EXPANDIR in-place
3. El gráfico se reemplaza por uno interactivo NVD3.js
4. Haz clic en ↙ Volver para colapsar de nuevo

✨ NO se abre ventana modal - Todo ocurre en el mismo lugar
"""

ctk.CTkLabel(
    main_frame,
    text=instrucciones,
    font=('Montserrat', 12),
    justify='left'
).pack(pady=10)

# Separador
ctk.CTkLabel(main_frame, text="─" * 100, font=('Montserrat', 12)).pack(pady=10)

# Contenedor para gráfico
chart_container = ctk.CTkFrame(main_frame, fg_color='transparent')
chart_container.pack(fill='both', expand=True, pady=10)

# Crear gráfico con motor NVD3
print("🎨 Creando gráfico con motor NVD3.js...")
chart = InteractiveChartCard(
    chart_container,
    title='Ventas Trimestrales 2025',
    width=1100,
    height=550,
    chart_engine='nvd3'  # ← Motor NVD3.js (componentes reutilizables)
)
chart.pack(fill='both', expand=True)

# Datos de ejemplo
datos = {
    'labels': ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025'],
    'values': [2500, 3200, 2900, 4100]
}

# Establecer datos
chart.set_chart('bar', datos)

# Separador
ctk.CTkLabel(main_frame, text="─" * 100, font=('Montserrat', 12)).pack(pady=10)

# Botones de prueba
buttons_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
buttons_frame.pack(pady=10)

def cambiar_datos():
    """Cambiar datos del gráfico"""
    import random
    nuevos_datos = {
        'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
        'values': [random.randint(2000, 5000) for _ in range(4)]
    }
    chart.set_chart('bar', nuevos_datos)
    print("📊 Datos actualizados")

ctk.CTkButton(
    buttons_frame,
    text="🔄 Cambiar Datos",
    command=cambiar_datos,
    width=150,
    height=40,
    font=('Montserrat', 13, 'bold')
).pack(side='left', padx=10)

ctk.CTkButton(
    buttons_frame,
    text="❌ Cerrar",
    command=root.destroy,
    width=150,
    height=40,
    font=('Montserrat', 13, 'bold'),
    fg_color='gray'
).pack(side='left', padx=10)

# Mensaje en consola
print("""
╔════════════════════════════════════════════════════════════╗
║  TEST EXPANSIÓN IN-PLACE - INSTRUCCIONES                  ║
╚════════════════════════════════════════════════════════════╝

✅ Gráfico creado con motor NVD3.js

📝 CÓMO PROBAR:
1. Observa el gráfico Matplotlib estático inicial
2. Haz clic en el botón ↗ (arriba a la derecha del gráfico)
3. El gráfico se EXPANDE in-place a NVD3.js interactivo
4. Interactúa con el gráfico (hover, tooltips)
5. Haz clic en ↙ Volver para colapsar

❌ NO SE ABRE VENTANA MODAL - Todo pasa in-place

🔵 Usando NVD3.js - Componentes reutilizables y rápidos
""")

root.mainloop()
