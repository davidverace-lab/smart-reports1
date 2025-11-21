"""
Ejemplo de uso de NVD3.js con el modal D3 Fullscreen
Demuestra cómo usar el motor NVD3 vs D3 puro
"""
import customtkinter as ctk
from smart_reports.ui.components.charts.modal_d3_fullscreen import show_d3_chart
from smart_reports.config.gestor_temas import get_theme_manager

# Crear ventana principal
root = ctk.CTk()
root.title("Demo NVD3.js vs D3.js")
root.geometry("900x700")

# Configurar tema
theme_manager = get_theme_manager()
theme_manager.set_theme('dark')

# Frame principal
frame = ctk.CTkFrame(root)
frame.pack(fill='both', expand=True, padx=30, pady=30)

# Título
ctk.CTkLabel(
    frame,
    text="🎨 Demo: NVD3.js vs D3.js",
    font=('Montserrat', 32, 'bold')
).pack(pady=20)

# Descripción
desc_text = """
Compara los dos motores de renderizado disponibles:

• NVD3.js (Default): Componentes reutilizables, desarrollo rápido
• D3.js Puro: Máxima personalización, control total

Haz clic en los botones para ver la diferencia.
"""
ctk.CTkLabel(
    frame,
    text=desc_text,
    font=('Montserrat', 14),
    justify='left'
).pack(pady=10)

# Datos de ejemplo
datos_ejemplo = {
    'labels': ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E'],
    'values': [150, 280, 190, 340, 220]
}

# Separador
ctk.CTkLabel(frame, text="─" * 80, font=('Montserrat', 12)).pack(pady=15)

# ============================================================
# SECCIÓN NVD3.js
# ============================================================
nvd3_frame = ctk.CTkFrame(frame, fg_color='#1a4d7a')
nvd3_frame.pack(fill='x', pady=10, padx=20)

ctk.CTkLabel(
    nvd3_frame,
    text="🔵 NVD3.js (Componentes Reutilizables)",
    font=('Montserrat', 20, 'bold'),
    text_color='white'
).pack(pady=15)

ctk.CTkLabel(
    nvd3_frame,
    text="✅ Menos código  ✅ Desarrollo rápido  ✅ Tooltips avanzados  ✅ Recomendado",
    font=('Montserrat', 11),
    text_color='#33C7F0'
).pack(pady=5)

# Botones NVD3
nvd3_buttons = ctk.CTkFrame(nvd3_frame, fg_color='transparent')
nvd3_buttons.pack(pady=15)

def nvd3_bar():
    show_d3_chart(root, "Ventas por Producto (NVD3)", "bar", datos_ejemplo, engine='nvd3')

def nvd3_donut():
    show_d3_chart(root, "Distribución (NVD3)", "donut", datos_ejemplo, engine='nvd3')

def nvd3_line():
    show_d3_chart(root, "Tendencia (NVD3)", "line", datos_ejemplo, engine='nvd3')

def nvd3_area():
    show_d3_chart(root, "Área de Ventas (NVD3)", "area", datos_ejemplo, engine='nvd3')

ctk.CTkButton(nvd3_buttons, text="📊 Barras NVD3", command=nvd3_bar, width=180, height=40).pack(side='left', padx=5)
ctk.CTkButton(nvd3_buttons, text="🍩 Dona NVD3", command=nvd3_donut, width=180, height=40).pack(side='left', padx=5)
ctk.CTkButton(nvd3_buttons, text="📈 Líneas NVD3", command=nvd3_line, width=180, height=40).pack(side='left', padx=5)
ctk.CTkButton(nvd3_buttons, text="🌊 Área NVD3", command=nvd3_area, width=180, height=40).pack(side='left', padx=5)

# ============================================================
# SECCIÓN D3.js
# ============================================================
d3_frame = ctk.CTkFrame(frame, fg_color='#4a1a7a')
d3_frame.pack(fill='x', pady=10, padx=20)

ctk.CTkLabel(
    d3_frame,
    text="🟣 D3.js Puro (Máxima Personalización)",
    font=('Montserrat', 20, 'bold'),
    text_color='white'
).pack(pady=15)

ctk.CTkLabel(
    d3_frame,
    text="⭐ Control total  ⭐ D3 v7  ⭐ Animaciones custom  ⭐ Efectos únicos",
    font=('Montserrat', 11),
    text_color='#D4A0FF'
).pack(pady=5)

# Botones D3
d3_buttons = ctk.CTkFrame(d3_frame, fg_color='transparent')
d3_buttons.pack(pady=15)

def d3_bar():
    show_d3_chart(root, "Ventas por Producto (D3)", "bar", datos_ejemplo, engine='d3')

def d3_donut():
    show_d3_chart(root, "Distribución (D3)", "donut", datos_ejemplo, engine='d3')

def d3_line():
    show_d3_chart(root, "Tendencia (D3)", "line", datos_ejemplo, engine='d3')

def d3_area():
    show_d3_chart(root, "Área de Ventas (D3)", "area", datos_ejemplo, engine='d3')

ctk.CTkButton(d3_buttons, text="📊 Barras D3", command=d3_bar, width=180, height=40).pack(side='left', padx=5)
ctk.CTkButton(d3_buttons, text="🍩 Dona D3", command=d3_donut, width=180, height=40).pack(side='left', padx=5)
ctk.CTkButton(d3_buttons, text="📈 Líneas D3", command=d3_line, width=180, height=40).pack(side='left', padx=5)
ctk.CTkButton(d3_buttons, text="🌊 Área D3", command=d3_area, width=180, height=40).pack(side='left', padx=5)

# Separador
ctk.CTkLabel(frame, text="─" * 80, font=('Montserrat', 12)).pack(pady=15)

# Nota informativa
info_frame = ctk.CTkFrame(frame, fg_color='#2a3a2a')
info_frame.pack(fill='x', pady=10, padx=20)

info_text = """
💡 RECOMENDACIÓN:
• Para dashboards empresariales → NVD3.js (default)
• Para visualizaciones únicas → D3.js puro

📖 Documentación completa: docs/D3_VS_NVD3.md
"""

ctk.CTkLabel(
    info_frame,
    text=info_text,
    font=('Montserrat', 12),
    justify='left',
    text_color='#90EE90'
).pack(pady=15, padx=20)

# Botón cerrar
ctk.CTkButton(
    frame,
    text="Cerrar",
    command=root.destroy,
    width=150,
    height=40,
    fg_color='gray'
).pack(pady=20)

root.mainloop()
