#!/usr/bin/env python3
"""
Test visual de gráficos - Muestra ventana con gráficos reales
"""
import customtkinter as ctk
from interfaz.componentes.visualizacion.tarjeta_d3_profesional import ProfessionalD3ChartCard

# Datos de prueba
datos_barras = {
    'labels': ['ICAVE', 'EIT', 'LCT', 'TIMSA', 'HPMX', 'TNG'],
    'values': [450, 320, 280, 190, 150, 98]
}

datos_donut = {
    'labels': ['Operaciones', 'Mantenimiento', 'Logística', 'Administración'],
    'values': [450, 320, 280, 150]
}

datos_lineas = {
    'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    'series': [
        {'name': 'Importaciones', 'values': [120, 150, 130, 180, 200, 190]},
        {'name': 'Exportaciones', 'values': [80, 95, 110, 120, 140, 155]}
    ]
}

class TestWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🎨 Test de Gráficos - Smart Reports")
        self.geometry("1200x800")

        # Configurar grid
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Título
        title = ctk.CTkLabel(
            self,
            text="✅ GRÁFICOS MATPLOTLIB EMBEBIDOS - FUNCIONANDO",
            font=('Montserrat', 20, 'bold'),
            text_color='#009BDE'
        )
        title.grid(row=0, column=0, columnspan=2, pady=20, sticky='ew')

        # Gráfico de barras
        card_barras = ProfessionalD3ChartCard(
            self,
            title="📊 Distribución por Unidad de Negocio"
        )
        card_barras.grid(row=1, column=0, padx=20, pady=10, sticky='nsew')
        card_barras.set_d3_chart('bar', datos_barras)

        # Gráfico donut
        card_donut = ProfessionalD3ChartCard(
            self,
            title="🍩 Distribución por Área"
        )
        card_donut.grid(row=1, column=1, padx=20, pady=10, sticky='nsew')
        card_donut.set_d3_chart('donut', datos_donut)

        # Gráfico de líneas
        card_lineas = ProfessionalD3ChartCard(
            self,
            title="📈 Evolución Mensual"
        )
        card_lineas.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky='nsew')
        card_lineas.set_d3_chart('line', datos_lineas)

        # Instrucciones
        instrucciones = ctk.CTkLabel(
            self,
            text="💡 Gráficos embebidos con matplotlib | Botón 'D3' para versión interactiva en navegador",
            font=('Montserrat', 11),
            text_color='#a0a0b0'
        )
        instrucciones.grid(row=3, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 INICIANDO TEST VISUAL DE GRÁFICOS")
    print("=" * 60)
    print("\n✅ Se abrirá una ventana con 3 gráficos:")
    print("   1. Gráfico de barras (superior izquierda)")
    print("   2. Gráfico donut (superior derecha)")
    print("   3. Gráfico de líneas (inferior)")
    print("\n💡 Características:")
    print("   - Gráficos matplotlib embebidos nativamente")
    print("   - Botón 'D3' para ver versión interactiva D3.js")
    print("   - Colores corporativos Hutchison Ports")
    print("\n" + "=" * 60)

    app = TestWindow()
    app.mainloop()
