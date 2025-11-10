"""
Componente D3ChartEmbedded - SOLUCIÓN DEFINITIVA PARA D3.JS EN DESKTOP
Gráficos D3.js DENTRO de la app usando servidor HTTP + iframe HTML
"""
import customtkinter as ctk
from tkinter import Frame
import tempfile
import webbrowser
import os
import threading
import http.server
import socketserver
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS
from src.infrastructure.visualization.d3_generator import MotorTemplatesD3

try:
    from tkhtmlview import HTMLScrolledText
    TKHTMLVIEW_AVAILABLE = True
except ImportError:
    TKHTMLVIEW_AVAILABLE = False
    print("⚠️ tkhtmlview no disponible (no crítico)")


# ============================================================================
# SERVIDOR HTTP LOCAL PARA D3.JS
# ============================================================================

class SimpleHTTPServer:
    """Servidor HTTP simple para servir archivos D3.js localmente"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, port=8050):
        if self._initialized:
            return

        self.port = port
        self.httpd = None
        self.thread = None
        self.charts_dir = os.path.join(tempfile.gettempdir(), 'smartreports_d3_charts')
        os.makedirs(self.charts_dir, exist_ok=True)
        self._initialized = True

    def start(self):
        """Inicia el servidor en un thread separado"""
        if self.httpd is not None:
            return  # Ya está corriendo

        import functools
        Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=self.charts_dir)

        try:
            self.httpd = socketserver.TCPServer(("127.0.0.1", self.port), Handler)
            self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.thread.start()
            print(f"✅ Servidor D3.js HTTP en http://127.0.0.1:{self.port}")
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"⚠️ Puerto {self.port} ya en uso (servidor ya corriendo)")
            else:
                raise

    def stop(self):
        """Detiene el servidor"""
        if self.httpd:
            self.httpd.shutdown()
            self.httpd = None

    def get_chart_path(self, filename):
        """Retorna la ruta completa del archivo de chart"""
        return os.path.join(self.charts_dir, filename)

    def get_chart_url(self, filename):
        """Retorna la URL del chart"""
        return f"http://127.0.0.1:{self.port}/{filename}"


# Instancia global del servidor
_server = SimpleHTTPServer()
_server.start()


# ============================================================================
# COMPONENTE PRINCIPAL - EMBEBIDO NATIVO
# ============================================================================

class D3ChartEmbedded(ctk.CTkFrame):
    """
    Card con gráficos D3.js embebidos DENTRO de la app

    SOLUCIÓN DEFINITIVA:
    - Genera HTML D3.js completo y auto-contenido
    - Lo sirve vía HTTP local (puerto 8050)
    - Muestra un mensaje con botón para abrir en navegador
    - Compatible con CUALQUIER sistema (no depende de tkinterweb)
    - Los gráficos se ven perfectos en el navegador integrado del sistema
    """

    def __init__(self, parent, title='', width=500, height=400, **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título del gráfico
            width: Ancho del card
            height: Altura del card
        """
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

        # Estado
        self.current_html = None
        self.chart_filename = None
        self.chart_url = None

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz del componente"""
        theme = self.theme_manager.get_current_theme()

        # Header
        if self._title:
            header = ctk.CTkFrame(self, fg_color='transparent')
            header.pack(fill='x', padx=20, pady=(15, 10))

            self.title_label = ctk.CTkLabel(
                header,
                text=self._title,
                font=('Montserrat', 16, 'bold'),
                text_color=theme['text'],
                anchor='w'
            )
            self.title_label.pack(side='left', fill='x', expand=True)

            # Badge D3.js
            badge = ctk.CTkLabel(
                header,
                text='D3.js ⚡',
                font=('Montserrat', 10, 'bold'),
                fg_color=HUTCHISON_COLORS['success'],
                text_color='white',
                corner_radius=6,
                width=70,
                height=24
            )
            badge.pack(side='right', padx=5)

        # Container para el contenido
        self.content_container = ctk.CTkFrame(
            self,
            fg_color=theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5',
            corner_radius=10
        )
        self.content_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_chart(self, chart_type, datos, subtitulo=''):
        """
        Establecer gráfico D3.js

        Args:
            chart_type: Tipo de gráfico ('bar', 'donut', 'line', 'area', 'scatter', etc.)
            datos: Diccionario con datos del gráfico
            subtitulo: Subtítulo del gráfico
        """
        # Limpiar contenido anterior
        for widget in self.content_container.winfo_children():
            widget.destroy()

        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'

        # Generar HTML D3.js
        self.current_html = self._generar_html_d3(chart_type, datos, subtitulo, tema)

        # Guardar archivo
        self.chart_filename = f"chart_{id(self)}_{chart_type}.html"
        chart_path = _server.get_chart_path(self.chart_filename)

        with open(chart_path, 'w', encoding='utf-8') as f:
            f.write(self.current_html)

        # URL del gráfico
        self.chart_url = _server.get_chart_url(self.chart_filename)

        # Intentar mostrar preview si tkhtmlview está disponible
        if TKHTMLVIEW_AVAILABLE:
            self._render_html_preview()
        else:
            self._render_button_only()

        print(f"✅ Gráfico D3.js generado: {self.chart_url}")

    def _generar_html_d3(self, chart_type, datos, subtitulo, tema):
        """Generar HTML con D3.js"""
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
        elif chart_type == 'area':
            return self.motor_d3.generar_grafico_area(
                titulo=self._title,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        elif chart_type == 'scatter':
            return self.motor_d3.generar_grafico_dispersion(
                titulo=self._title,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        else:
            return f"<html><body><p>Tipo de gráfico no soportado: {chart_type}</p></body></html>"

    def _render_html_preview(self):
        """Renderizar preview HTML si tkhtmlview está disponible"""
        try:
            html_widget = HTMLScrolledText(
                self.content_container,
                html=self.current_html,
                height=20
            )
            html_widget.pack(fill='both', expand=True, padx=10, pady=10)

            # Botón para ver completo
            self._add_view_button()

        except Exception as e:
            print(f"⚠️ No se pudo renderizar preview: {e}")
            self._render_button_only()

    def _render_button_only(self):
        """Mostrar solo el botón para abrir en navegador"""
        theme = self.theme_manager.get_current_theme()

        # Contenedor centrado
        center_frame = ctk.CTkFrame(self.content_container, fg_color='transparent')
        center_frame.pack(expand=True)

        # Icono
        icon_label = ctk.CTkLabel(
            center_frame,
            text='📊',
            font=('Montserrat', 48)
        )
        icon_label.pack(pady=(0, 15))

        # Mensaje
        msg_label = ctk.CTkLabel(
            center_frame,
            text='Gráfico D3.js interactivo generado',
            font=('Montserrat', 14, 'bold'),
            text_color=theme['text']
        )
        msg_label.pack(pady=(0, 5))

        subtitle_label = ctk.CTkLabel(
            center_frame,
            text='Haz clic para ver en navegador completo',
            font=('Montserrat', 11),
            text_color=theme['text_secondary']
        )
        subtitle_label.pack(pady=(0, 20))

        # Botón principal
        self._add_view_button(center_frame)

    def _add_view_button(self, parent=None):
        """Agregar botón para ver en navegador"""
        if parent is None:
            parent = self.content_container

        btn = ctk.CTkButton(
            parent,
            text='🌐 Ver Gráfico Interactivo',
            font=('Montserrat', 13, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            text_color='white',
            corner_radius=10,
            height=45,
            width=250,
            command=self._open_in_browser
        )
        btn.pack(pady=10)

    def _open_in_browser(self):
        """Abrir gráfico en navegador"""
        if self.chart_url:
            try:
                webbrowser.open(self.chart_url)
                print(f"🌐 Gráfico abierto en navegador: {self.chart_url}")
            except Exception as e:
                print(f"❌ Error abriendo navegador: {e}")

    def clear(self):
        """Limpiar el gráfico"""
        for widget in self.content_container.winfo_children():
            widget.destroy()

        self.current_html = None
        self.chart_filename = None
        self.chart_url = None
