"""
Modal Fullscreen D3.js/NVD3.js - Gráficos Interactivos Embebidos
✨ CARACTERÍSTICAS:
- Ventana modal con gráficos D3.js/NVD3.js interactivos
- Embebido dentro de la aplicación (NO navegador externo)
- Animación de entrada deslizante desde abajo
- Botón cerrar elegante (X) + tecla ESC
- Zoom, pan, tooltips, filtros interactivos
- Soporte para: bar, donut, line, area, horizontal_bar
- Motor dual: D3.js puro o NVD3.js (componentes reutilizables)
"""
import customtkinter as ctk
from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.config.themes import HUTCHISON_COLORS
from smart_reports.utils.visualization.d3_generator import MotorTemplatesD3
from smart_reports.utils.visualization.nvd3_generator import MotorTemplatesNVD3
import os
import tempfile

try:
    from tkinterweb import HtmlFrame
    TKINTERWEB_AVAILABLE = True
except ImportError:
    TKINTERWEB_AVAILABLE = False
    print("⚠️ tkinterweb no disponible - Modal D3.js deshabilitado")


class ModalD3Fullscreen(ctk.CTkToplevel):
    """Modal fullscreen para mostrar gráficos D3.js/NVD3.js interactivos embebidos"""

    def __init__(self, parent, title, chart_type, chart_data, engine='nvd3', **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título del gráfico
            chart_type: Tipo de gráfico ('bar', 'donut', 'line', 'area')
            chart_data: Datos del gráfico {'labels': [...], 'values': [...]}
            engine: Motor de renderizado - 'nvd3' (default) o 'd3'
        """
        super().__init__(parent, **kwargs)

        if not TKINTERWEB_AVAILABLE:
            self.destroy()
            raise ImportError("tkinterweb no está instalado. Instala con: pip install tkinterweb")

        self.theme_manager = get_theme_manager()
        self.title_text = title
        self.chart_type = chart_type
        self.chart_data = chart_data
        self.engine = engine  # 'nvd3' o 'd3'

        # Referencias
        self.html_frame = None
        self.temp_file = None

        # Configurar ventana modal
        self._setup_window()
        self._create_ui()
        self._render_d3_chart()
        self._animate_entrance()

        # Capturar tecla ESC
        self.bind('<Escape>', lambda e: self._close_modal())

    def _setup_window(self):
        """Configurar ventana modal"""
        # Fullscreen
        self.attributes('-fullscreen', False)
        self.attributes('-topmost', True)

        # Tamaño casi fullscreen (95% de la pantalla)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = int(screen_width * 0.95)
        height = int(screen_height * 0.95)

        # Centrar
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

        # Estilo
        theme = self.theme_manager.get_current_theme()
        self.configure(fg_color=theme['colors']['background'])

        # Título de ventana
        self.title(f"📊 {self.title_text} - D3.js Interactivo")

    def _create_ui(self):
        """Crear interfaz del modal"""
        theme = self.theme_manager.get_current_theme()

        # === HEADER CON TÍTULO Y BOTÓN CERRAR ===
        header = ctk.CTkFrame(
            self,
            fg_color=HUTCHISON_COLORS['primary'],
            height=80,
            corner_radius=0
        )
        header.pack(fill='x', side='top')
        header.pack_propagate(False)

        # Botón cerrar (izquierda)
        close_btn = ctk.CTkButton(
            header,
            text="✕",
            width=60,
            height=60,
            font=("Montserrat", 30, "bold"),
            fg_color="transparent",
            hover_color=theme['colors']['error'],
            command=self._close_modal
        )
        close_btn.pack(side='left', padx=10, pady=10)

        # Título (centro)
        title_label = ctk.CTkLabel(
            header,
            text=self.title_text,
            font=("Montserrat", 28, "bold"),
            text_color="white"
        )
        title_label.pack(side='left', expand=True, pady=10)

        # Badge "NVD3.js Interactive" o "D3.js Interactive"
        badge_text = "NVD3.js Interactive" if self.engine == 'nvd3' else "D3.js Interactive"
        badge = ctk.CTkLabel(
            header,
            text=badge_text,
            font=("Montserrat", 11, "bold"),
            text_color="white",
            fg_color=HUTCHISON_COLORS['aqua_green'],
            corner_radius=12,
            padx=15,
            pady=5
        )
        badge.pack(side='right', padx=20, pady=10)

        # === CONTENEDOR PRINCIPAL ===
        self.main_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)

    def _render_d3_chart(self):
        """Renderizar gráfico D3.js usando tkinterweb"""
        try:
            print(f"  🔧 Generando HTML D3.js para tipo: {self.chart_type}")

            # Generar HTML con D3.js
            html_content = self._generate_d3_html()

            print(f"  ✅ HTML generado: {len(html_content)} caracteres")

            # Verificar que el HTML contiene elementos clave
            if 'd3.v7.min.js' not in html_content:
                raise ValueError("HTML no contiene referencia a D3.js")

            if 'chart-container' not in html_content:
                raise ValueError("HTML no contiene chart-container")

            # Crear HtmlFrame
            print("  🔧 Creando HtmlFrame...")
            self.html_frame = HtmlFrame(
                self.main_container,
                messages_enabled=False
            )
            self.html_frame.pack(fill='both', expand=True)

            print("  🔧 Cargando HTML en HtmlFrame...")
            # Cargar HTML (load_html renderiza directamente el string)
            self.html_frame.load_html(html_content)

            print("  ✅ Gráfico D3.js renderizado exitosamente")

        except Exception as e:
            print(f"❌ Error renderizando D3.js: {e}")
            import traceback
            traceback.print_exc()

            # Mostrar mensaje de error detallado
            error_label = ctk.CTkLabel(
                self.main_container,
                text=f"⚠️ Error al cargar gráfico D3.js:\n{str(e)}\n\nVerifica:\n1. tkinterweb instalado (pip install tkinterweb>=3.23.0)\n2. Conexión a internet (para cargar D3.js desde CDN)\n3. Datos del gráfico válidos",
                font=("Montserrat", 12),
                text_color="red",
                justify="left"
            )
            error_label.pack(expand=True, padx=20, pady=20)

    def _generate_d3_html(self) -> str:
        """Generar HTML con D3.js o NVD3.js según el tipo de gráfico"""
        # Determinar tema
        theme = self.theme_manager.get_current_theme()
        chart_theme = 'dark' if theme['name'] == 'dark' else 'light'

        # Seleccionar motor de templates
        Motor = MotorTemplatesNVD3 if self.engine == 'nvd3' else MotorTemplatesD3

        # Mensajes según motor
        if self.engine == 'nvd3':
            subtitulos = {
                'bar': "Gráfico interactivo con NVD3.js - Componentes reutilizables sobre D3.js",
                'donut': "Gráfico de dona con NVD3.js - Pasa el mouse sobre las secciones",
                'line': "Gráfico de líneas con NVD3.js - Interfaz interactiva avanzada",
                'area': "Gráfico de área con NVD3.js - Cambia el estilo con los botones"
            }
        else:
            subtitulos = {
                'bar': "Gráfico interactivo con D3.js - Puedes hacer clic en los botones para ordenar",
                'donut': "Pasa el mouse sobre las secciones para ver detalles",
                'line': "Pasa el mouse sobre los puntos para ver valores",
                'area': "Gráfico de área con D3.js"
            }

        # Generar HTML según tipo de gráfico
        if self.chart_type in ['bar', 'horizontal_bar']:
            html = Motor.generar_grafico_barras(
                titulo=self.title_text,
                datos=self.chart_data,
                subtitulo=subtitulos.get('bar', ''),
                tema=chart_theme,
                interactivo=True if self.engine == 'd3' else None
            )
        elif self.chart_type == 'donut':
            html = Motor.generar_grafico_donut(
                titulo=self.title_text,
                datos=self.chart_data,
                subtitulo=subtitulos.get('donut', ''),
                tema=chart_theme
            )
        elif self.chart_type == 'line':
            html = Motor.generar_grafico_lineas(
                titulo=self.title_text,
                datos=self.chart_data,
                subtitulo=subtitulos.get('line', ''),
                tema=chart_theme
            )
        elif self.chart_type == 'area':
            html = Motor.generar_grafico_area(
                titulo=self.title_text,
                datos=self.chart_data,
                subtitulo=subtitulos.get('area', ''),
                tema=chart_theme
            )
        else:
            # Tipo desconocido, usar barras por defecto
            html = Motor.generar_grafico_barras(
                titulo=self.title_text,
                datos=self.chart_data,
                tema=chart_theme
            )

        return html

    def _animate_entrance(self):
        """Animar entrada del modal deslizando desde abajo"""
        # Guardar posición final
        final_geometry = self.geometry()

        # Posición inicial (fuera de pantalla, abajo)
        screen_height = self.winfo_screenheight()
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{self.winfo_x()}+{screen_height}")

        # Actualizar para que se dibuje
        self.update()

        # Animar deslizamiento hacia arriba
        self._animate_slide_up(final_geometry)

    def _animate_slide_up(self, final_geometry, steps=20, delay=10):
        """Animar deslizamiento hacia arriba"""
        # Extraer posición final
        parts = final_geometry.split('+')
        final_y = int(parts[-1])

        # Posición actual
        current_y = self.winfo_y()

        # Calcular paso
        step = (current_y - final_y) // steps

        def animate(current_step=0):
            if current_step >= steps:
                # Establecer posición final exacta
                self.geometry(final_geometry)
                return

            # Calcular nueva posición
            new_y = current_y - (step * (current_step + 1))
            self.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{self.winfo_x()}+{new_y}")

            # Siguiente paso
            self.after(delay, lambda: animate(current_step + 1))

        animate()

    def _close_modal(self):
        """Cerrar modal con animación de salida"""
        # Animación de desvanecimiento
        self.attributes('-alpha', 0.8)
        self.after(50, lambda: self.attributes('-alpha', 0.6))
        self.after(100, lambda: self.attributes('-alpha', 0.4))
        self.after(150, lambda: self.attributes('-alpha', 0.2))
        self.after(200, lambda: self._destroy_modal())

    def _destroy_modal(self):
        """Destruir modal y limpiar recursos"""
        # Limpiar archivo temporal si existe
        if self.temp_file and os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
            except:
                pass

        self.destroy()


# ============================================================================
# FUNCIÓN DE CONVENIENCIA
# ============================================================================

def show_d3_chart(parent, title: str, chart_type: str, chart_data: dict, engine: str = 'nvd3'):
    """
    Mostrar gráfico D3.js/NVD3.js en modal fullscreen

    Args:
        parent: Widget padre (ventana principal)
        title: Título del gráfico
        chart_type: Tipo de gráfico ('bar', 'donut', 'line', 'area', 'horizontal_bar')
        chart_data: Datos del gráfico {'labels': [...], 'values': [...]}
        engine: Motor de renderizado - 'nvd3' (default) o 'd3'

    Example:
        # Usando NVD3.js (componentes reutilizables)
        show_d3_chart(
            parent=self.master,
            title="Ventas por Producto",
            chart_type="bar",
            chart_data={'labels': ['A', 'B', 'C'], 'values': [10, 20, 30]},
            engine='nvd3'
        )

        # Usando D3.js puro (máxima personalización)
        show_d3_chart(
            parent=self.master,
            title="Ventas por Producto",
            chart_type="bar",
            chart_data={'labels': ['A', 'B', 'C'], 'values': [10, 20, 30]},
            engine='d3'
        )
    """
    if not TKINTERWEB_AVAILABLE:
        print("⚠️ tkinterweb no está disponible - No se puede mostrar modal D3.js")
        return

    modal = ModalD3Fullscreen(parent, title, chart_type, chart_data, engine=engine)
    modal.focus()
    modal.grab_set()  # Modal verdadero (bloquea ventana padre)
