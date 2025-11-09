"""
Componente ProfessionalD3ChartCard - SOLUCIÓN DEFINITIVA
Gráficos D3.js interactivos DENTRO de la app con servidor HTTP local
"""
import customtkinter as ctk
from tkinter import Frame
import tempfile
import webbrowser
import os
import threading
import http.server
import socketserver
from nucleo.configuracion.gestor_temas import get_theme_manager
from nucleo.configuracion.ajustes import HUTCHISON_COLORS
from nucleo.servicios.motor_templates_d3 import MotorTemplatesD3
from nucleo.servicios.motor_graficos_matplotlib import MotorGraficosMatplotlib

# Intentar importar tkinterweb para renderizar HTML con JavaScript
try:
    from tkinterweb import HtmlFrame
    TKINTERWEB_AVAILABLE = True
except ImportError:
    TKINTERWEB_AVAILABLE = False
    print("⚠️ tkinterweb no disponible. Instala con: pip install tkinterweb")
    print("   Usando matplotlib como fallback...")


# ============================================================================
# SERVIDOR HTTP LOCAL PARA D3.JS
# ============================================================================

class SimpleHTTPServer:
    """Servidor HTTP simple para servir archivos D3.js localmente"""

    def __init__(self, directory, port=8050):
        self.directory = directory
        self.port = port
        self.httpd = None
        self.thread = None

    def start(self):
        """Inicia el servidor en un thread separado"""
        if self.httpd is not None:
            return  # Ya está corriendo

        original_dir = os.getcwd()
        os.chdir(self.directory)

        Handler = http.server.SimpleHTTPRequestHandler

        try:
            self.httpd = socketserver.TCPServer(("", self.port), Handler)
            self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.thread.start()
            print(f"✅ Servidor HTTP D3.js iniciado en http://localhost:{self.port}")
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"⚠️ Puerto {self.port} ya en uso (servidor ya corriendo)")
            else:
                raise
        finally:
            os.chdir(original_dir)

    def stop(self):
        """Detiene el servidor"""
        if self.httpd:
            self.httpd.shutdown()
            self.httpd = None
            print("✅ Servidor HTTP detenido")


# Servidor global compartido por todos los gráficos
_GLOBAL_SERVER = None


def get_http_server():
    """Obtiene o crea el servidor HTTP global"""
    global _GLOBAL_SERVER
    if _GLOBAL_SERVER is None:
        temp_dir = tempfile.gettempdir()
        charts_dir = os.path.join(temp_dir, 'smartreports_d3_charts')
        os.makedirs(charts_dir, exist_ok=True)
        _GLOBAL_SERVER = SimpleHTTPServer(charts_dir, port=8050)
        _GLOBAL_SERVER.start()
    return _GLOBAL_SERVER


# ============================================================================
# COMPONENTE PRINCIPAL
# ============================================================================

class ProfessionalD3ChartCard(ctk.CTkFrame):
    """
    Card profesional con gráficos D3.js interactivos DENTRO de la app

    SOLUCIÓN DEFINITIVA:
    - Usa servidor HTTP local para servir D3.js
    - tkinterweb carga desde http://localhost (ejecuta JavaScript)
    - Fallback a matplotlib si tkinterweb no está disponible
    """

    def __init__(self, parent, title='', width=500, height=400, **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título del gráfico
            width: Ancho del card
            height: Altura del card
        """
        # Obtener tema actual
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border'],
            **kwargs
        )

        self._title = title
        self._width = width
        self._height = height
        self.motor_d3 = MotorTemplatesD3()
        self.motor_matplotlib = MotorGraficosMatplotlib()

        # Para D3.js interactivo
        self.server = None
        self.html_widget = None
        self.chart_filename = None

        # Para matplotlib (fallback)
        self.canvas_widget = None

        # Estado actual
        self.current_html_d3 = None
        self.current_chart_type = None
        self.current_datos = None
        self.using_d3 = TKINTERWEB_AVAILABLE  # True si podemos usar D3.js

        # Header
        if title:
            header = ctk.CTkFrame(self, fg_color='transparent')
            header.pack(fill='x', padx=20, pady=(15, 10))

            self.title_label = ctk.CTkLabel(
                header,
                text=title,
                font=('Montserrat', 16, 'bold'),
                text_color=theme['text'],
                anchor='w'
            )
            self.title_label.pack(side='left', fill='x', expand=True)

            # Badges y botones
            btn_frame = ctk.CTkFrame(header, fg_color='transparent')
            btn_frame.pack(side='right')

            # Badge según tecnología disponible
            if TKINTERWEB_AVAILABLE:
                badge_text = 'D3.js ⚡'
                badge_color = HUTCHISON_COLORS['success']
            else:
                badge_text = '📊 MPL'
                badge_color = HUTCHISON_COLORS['ports_sky_blue']

            self.badge = ctk.CTkLabel(
                btn_frame,
                text=badge_text,
                font=('Montserrat', 10, 'bold'),
                fg_color=badge_color,
                text_color='white',
                corner_radius=6,
                width=70,
                height=24
            )
            self.badge.pack(side='left', padx=5)

            # Botón para abrir en navegador externo
            self.browser_btn = ctk.CTkButton(
                btn_frame,
                text='🌐',
                font=('Montserrat', 12, 'bold'),
                fg_color=HUTCHISON_COLORS['ports_sky_blue'],
                hover_color=HUTCHISON_COLORS['ports_sea_blue'],
                text_color='white',
                corner_radius=6,
                width=35,
                height=28,
                command=self._open_in_browser
            )
            self.browser_btn.pack(side='left', padx=5)

        # Container para el gráfico
        chart_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.chart_container = ctk.CTkFrame(self, fg_color=chart_bg, corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_d3_chart(self, chart_type, datos, subtitulo=''):
        """
        Establecer gráfico (D3.js interactivo si disponible, sino matplotlib)

        Args:
            chart_type: Tipo de gráfico ('bar', 'donut', 'line')
            datos: Diccionario con datos del gráfico
            subtitulo: Subtítulo del gráfico
        """
        # Guardar datos para regenerar
        self.current_chart_type = chart_type
        self.current_datos = datos

        # Limpiar contenido anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        self.canvas_widget = None
        self.html_widget = None

        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'

        # Generar HTML D3.js (siempre lo generamos para botón de navegador)
        self.current_html_d3 = self._generar_html_d3(chart_type, datos, subtitulo, tema)

        # Decidir qué tecnología usar
        if TKINTERWEB_AVAILABLE:
            # OPCIÓN 1: D3.js interactivo con servidor HTTP (PREFERIDO)
            try:
                self._render_d3_with_http_server(chart_type, datos, subtitulo, tema)
                print(f"✅ Gráfico D3.js {chart_type} renderizado (interactivo)")
                self.using_d3 = True
                return
            except Exception as e:
                print(f"⚠️ Error con D3.js, usando matplotlib: {e}")
                self.using_d3 = False

        # OPCIÓN 2: Matplotlib fallback (siempre funciona)
        try:
            self._render_matplotlib(chart_type, datos, tema)
            print(f"✅ Gráfico {chart_type} renderizado con matplotlib")
            self.using_d3 = False
        except Exception as e:
            print(f"❌ Error renderizando matplotlib: {e}")
            import traceback
            traceback.print_exc()
            self._show_error(f"Error al generar gráfico: {e}")

    def _generar_html_d3(self, chart_type, datos, subtitulo, tema):
        """Generar HTML con D3.js para navegador"""
        if chart_type == 'bar':
            return self.motor_d3.generar_grafico_barras(
                titulo=self._title,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema,
                interactivo=True
            )
        elif chart_type == 'donut':
            return self.motor_d3.generar_grafico_donut(
                titulo=self._title,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        elif chart_type == 'line':
            return self.motor_d3.generar_grafico_lineas(
                titulo=self._title,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        else:
            return "<p>Tipo de gráfico no soportado</p>"

    def _render_d3_with_http_server(self, chart_type, datos, subtitulo, tema):
        """
        Renderiza D3.js usando servidor HTTP local + tkinterweb
        ESTO SÍ EJECUTA JAVASCRIPT porque carga desde http://localhost
        """
        # Iniciar servidor HTTP si no está corriendo
        if self.server is None:
            self.server = get_http_server()

        # Guardar HTML en carpeta del servidor
        self.chart_filename = f"chart_{id(self)}_{chart_type}.html"
        charts_dir = os.path.join(tempfile.gettempdir(), 'smartreports_d3_charts')
        html_path = os.path.join(charts_dir, self.chart_filename)

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(self.current_html_d3)

        # URL del gráfico
        chart_url = f"http://localhost:{self.server.port}/{self.chart_filename}"

        # Renderizar con tkinterweb
        html_container = Frame(self.chart_container, bg=self.chart_container._fg_color)
        html_container.pack(fill='both', expand=True, padx=5, pady=5)

        self.html_widget = HtmlFrame(
            html_container,
            messages_enabled=False,
            vertical_scrollbar=False,
            horizontal_scrollbar=False
        )

        # Cargar desde URL HTTP (esto permite ejecutar JavaScript)
        self.html_widget.load_url(chart_url)
        self.html_widget.pack(fill='both', expand=True)

        print(f"🌐 D3.js cargado desde: {chart_url}")

    def _render_matplotlib(self, chart_type, datos, tema):
        """Renderizar gráfico con matplotlib embebido nativamente"""
        # Container para matplotlib
        canvas_frame = Frame(self.chart_container, bg=self.chart_container._fg_color)
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Generar gráfico según tipo
        if chart_type == 'bar':
            canvas = self.motor_matplotlib.crear_grafico_barras(
                canvas_frame, datos, tema, titulo=''
            )
        elif chart_type == 'donut':
            canvas = self.motor_matplotlib.crear_grafico_donut(
                canvas_frame, datos, tema, titulo=''
            )
        elif chart_type == 'line':
            canvas = self.motor_matplotlib.crear_grafico_lineas(
                canvas_frame, datos, tema, titulo=''
            )
        else:
            raise ValueError(f"Tipo de gráfico no soportado: {chart_type}")

        if canvas:
            self.canvas_widget = canvas
            canvas.get_tk_widget().pack(fill='both', expand=True)
        else:
            raise ValueError("No se pudo generar el gráfico (datos vacíos)")

    def _open_in_browser(self):
        """Abrir gráfico en navegador externo completo"""
        if not self.current_html_d3:
            return

        try:
            # Si ya tenemos el archivo en el servidor, usar esa URL
            if self.chart_filename and self.server:
                url = f"http://localhost:{self.server.port}/{self.chart_filename}"
                webbrowser.open(url)
                print(f"🌐 Gráfico abierto en navegador: {url}")
            else:
                # Crear archivo temporal
                temp_file = tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix='.html',
                    delete=False,
                    encoding='utf-8'
                )
                temp_file.write(self.current_html_d3)
                temp_file.close()

                # Abrir en navegador
                webbrowser.open('file://' + temp_file.name)
                print(f"🌐 Gráfico D3.js abierto en navegador externo")
        except Exception as e:
            print(f"❌ Error abriendo en navegador: {e}")

    def _show_error(self, message):
        """Mostrar mensaje de error"""
        theme = self.theme_manager.get_current_theme()
        error_label = ctk.CTkLabel(
            self.chart_container,
            text=f'❌ {message}',
            font=('Montserrat', 12),
            text_color='#ff6b6b'
        )
        error_label.pack(expand=True, pady=20)

    def clear(self):
        """Limpiar el gráfico"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        # Limpiar referencias
        self.canvas_widget = None
        self.html_widget = None
        self.current_html_d3 = None
        self.current_chart_type = None
        self.current_datos = None

        # No eliminar archivo HTML (puede estar siendo usado por el navegador)
        # Se limpiará automáticamente cuando se cierre la app
