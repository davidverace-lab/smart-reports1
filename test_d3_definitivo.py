"""
Test definitivo para D3.js interactivo DENTRO de la app
Verifica que los gráficos D3.js se vean y funcionen correctamente
"""
import customtkinter as ctk
import sys
from pathlib import Path

# Agregar ruta del proyecto
sys.path.insert(0, str(Path(__file__).parent))

from interfaz.componentes.visualizacion.tarjeta_d3_profesional import (
    ProfessionalD3ChartCard,
    TKINTERWEB_AVAILABLE
)


class TestD3Window(ctk.CTk):
    """Ventana de prueba para gráficos D3.js"""

    def __init__(self):
        super().__init__()

        self.title("✅ Test D3.js Definitivo - Smart Reports")
        self.geometry("1400x900")

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ============================================================
        # HEADER CON INFO
        # ============================================================
        header = ctk.CTkFrame(self, fg_color="#1e3a5f", corner_radius=0)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

        title_label = ctk.CTkLabel(
            header,
            text="Test D3.js Definitivo - Smart Reports",
            font=("Montserrat", 20, "bold"),
            text_color="white"
        )
        title_label.pack(pady=15)

        # Estado de tkinterweb
        if TKINTERWEB_AVAILABLE:
            status_text = "✅ tkinterweb disponible - Gráficos D3.js interactivos ACTIVADOS"
            status_color = "#51cf66"
        else:
            status_text = "⚠️ tkinterweb no disponible - Usando matplotlib (fallback)"
            status_color = "#ffa94d"

        status_label = ctk.CTkLabel(
            header,
            text=status_text,
            font=("Montserrat", 12),
            text_color=status_color
        )
        status_label.pack(pady=(0, 10))

        if not TKINTERWEB_AVAILABLE:
            install_label = ctk.CTkLabel(
                header,
                text="Para activar D3.js: pip install tkinterweb",
                font=("Consolas", 10),
                text_color="#a0a0b0"
            )
            install_label.pack(pady=(0, 10))

        # ============================================================
        # GRÁFICOS
        # ============================================================

        # Datos de prueba
        datos_barras = {
            'categorias': ['ICAVE', 'EIT', 'LCT', 'TIMSA', 'HPMX', 'TNG'],
            'valores': [89, 76, 92, 68, 81, 95],
            'meta': 80
        }

        datos_donut = {
            'categorias': ['Completado', 'En Progreso', 'No Iniciado', 'Vencido'],
            'valores': [450, 230, 180, 140]
        }

        datos_lineas = {
            'categorias': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            'valores': [65, 72, 68, 85, 88, 92],
            'meta': 80
        }

        # Fila 1: Gráfico de barras y donut
        self.card_barras = ProfessionalD3ChartCard(
            self,
            title="📊 Cumplimiento por Unidad de Negocio",
            width=650,
            height=400
        )
        self.card_barras.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")

        self.card_donut = ProfessionalD3ChartCard(
            self,
            title="🍩 Distribución de Estatus",
            width=650,
            height=400
        )
        self.card_donut.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

        # Fila 2: Gráfico de líneas
        self.grid_rowconfigure(2, weight=1)
        self.card_lineas = ProfessionalD3ChartCard(
            self,
            title="📈 Tendencia de Cumplimiento Mensual",
            width=1320,
            height=400
        )
        self.card_lineas.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 15), sticky="nsew")

        # ============================================================
        # RENDERIZAR GRÁFICOS
        # ============================================================

        print("\n" + "="*60)
        print("INICIANDO TEST D3.JS DEFINITIVO")
        print("="*60)

        self.after(500, lambda: self._render_charts(
            datos_barras, datos_donut, datos_lineas
        ))

    def _render_charts(self, datos_barras, datos_donut, datos_lineas):
        """Renderiza los 3 gráficos"""
        try:
            print("\n🎨 Renderizando gráfico de barras...")
            self.card_barras.set_d3_chart(
                'bar',
                datos_barras,
                'Porcentaje de módulos completados por unidad'
            )

            print("🎨 Renderizando gráfico donut...")
            self.card_donut.set_d3_chart(
                'donut',
                datos_donut,
                'Estado de módulos asignados'
            )

            print("🎨 Renderizando gráfico de líneas...")
            self.card_lineas.set_d3_chart(
                'line',
                datos_lineas,
                'Evolución del cumplimiento durante 2024'
            )

            print("\n✅ TODOS LOS GRÁFICOS RENDERIZADOS")
            print("="*60)

            if TKINTERWEB_AVAILABLE:
                print("\n💡 INSTRUCCIONES:")
                print("   1. Los gráficos D3.js deben verse INTERACTIVOS")
                print("   2. Pasa el mouse sobre las barras/secciones")
                print("   3. Deberías ver tooltips con información")
                print("   4. Los gráficos deben tener animaciones suaves")
                print("   5. Usa el botón 🌐 para abrir en navegador completo")
            else:
                print("\n💡 MODO FALLBACK (matplotlib):")
                print("   1. Los gráficos se ven pero no son interactivos")
                print("   2. Instala tkinterweb para activar D3.js:")
                print("      pip install tkinterweb")

        except Exception as e:
            print(f"\n❌ ERROR renderizando gráficos: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("TEST D3.JS DEFINITIVO - SMART REPORTS")
    print("="*60)
    print(f"tkinterweb disponible: {TKINTERWEB_AVAILABLE}")
    print("="*60 + "\n")

    app = TestD3Window()
    app.mainloop()


if __name__ == "__main__":
    main()
