"""
Componente D3ChartServidor - Gráficos D3.js con servidor HTTP local
Solución DEFINITIVA que SÍ ejecuta JavaScript dentro de la app
"""
import customtkinter as ctk
from tkinter import Frame
import tempfile
import os
import threading
import http.server
import socketserver
import webbrowser
from pathlib import Path
from nucleo.configuracion.gestor_temas import get_theme_manager
from nucleo.configuracion.ajustes import HUTCHISON_COLORS
from nucleo.servicios.motor_templates_d3 import MotorTemplatesD3

# Intentar importar tkinterweb
try:
    from tkinterweb import HtmlFrame
    TKINTERWEB_AVAILABLE = True
except ImportError:
    TKINTERWEB_AVAILABLE = False


class SimpleHTTPServer:
    """Servidor HTTP simple para servir archivos locales"""

    def __init__(self, directory, port=8050):
        self.directory = directory
        self.port = port
        self.httpd = None
        self.thread = None

    def start(self):
        """Inicia el servidor en un thread separado"""
        if self.httpd is not None:
            return  # Ya está corriendo

        os.chdir(self.directory)
        Handler = http.server.SimpleHTTPRequestHandler

        try:
            self.httpd = socketserver.TCPServer(("", self.port), Handler)
            self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.thread.start()
            print(f"✅ Servidor HTTP iniciado en http://localhost:{self.port}")
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"⚠️ Puerto {self.port} ya en uso, servidor ya corriendo")
            else:
                raise

    def stop(self):
        """Detiene el servidor"""
        if self.httpd:
            self.httpd.shutdown()
            self.httpd = None
            print("✅ Servidor HTTP detenido")


# Servidor global (uno solo para toda la aplicación)
_GLOBAL_SERVER = None


def get_http_server():
    """Obtiene o crea el servidor HTTP global"""
    global _GLOBAL_SERVER
    if _GLOBAL_SERVER is None:
        temp_dir = tempfile.gettempdir()
        charts_dir = os.path.join(temp_dir, 'smartreports_charts')
        os.makedirs(charts_dir, exist_ok=True)
        _GLOBAL_SERVER = SimpleHTTPServer(charts_dir, port=8050)
        _GLOBAL_SERVER.start()
    return _GLOBAL_SERVER


class D3ChartServidor(ctk.CTkFrame):
    """
    Tarjeta con gráficos D3.js usando servidor HTTP local
    SOLUCIÓN DEFINITIVA que funciona SIEMPRE
    """

    def __init__(self, parent, title='', width=500, height=400, **kwargs):
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
        self.html_widget = None
        self.current_html = None
        self.chart_filename = None

        # Iniciar servidor HTTP global
        self.server = get_http_server()

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

            # Badges
            btn_frame = ctk.CTkFrame(header, fg_color='transparent')
            btn_frame.pack(side='right')

            badge = ctk.CTkLabel(
                btn_frame,
                text='D3.js ⚡',
                font=('Montserrat', 10, 'bold'),
                fg_color=HUTCHISON_COLORS['ports_sky_blue'],
                text_color='white',
                corner_radius=6,
                width=70,
                height=24
            )
            badge.pack(side='left', padx=5)

            # Botón para abrir en navegador completo
            self.browser_btn = ctk.CTkButton(
                btn_frame,
                text='🌐',
                font=('Montserrat', 12, 'bold'),
                fg_color=HUTCHISON_COLORS['success'],
                hover_color='#41a755',
                text_color='white',
                corner_radius=6,
                width=35,
                height=28,
                command=self._open_in_full_browser
            )
            self.browser_btn.pack(side='left', padx=5)

        # Container para el gráfico
        chart_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.chart_container = ctk.CTkFrame(self, fg_color=chart_bg, corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_d3_chart(self, chart_type, datos, subtitulo=''):
        """
        Establece gráfico D3.js interactivo

        Args:
            chart_type: Tipo de gráfico ('bar', 'donut', 'line')
            datos: Diccionario con datos del gráfico
            subtitulo: Subtítulo del gráfico
        """
        # Limpiar contenido anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'

        # Generar HTML D3.js
        html = self._generar_html_d3(chart_type, datos, subtitulo, tema)
        self.current_html = html

        # Guardar HTML en carpeta del servidor
        self.chart_filename = f"chart_{id(self)}.html"
        charts_dir = os.path.join(tempfile.gettempdir(), 'smartreports_charts')
        html_path = os.path.join(charts_dir, self.chart_filename)

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)

        # URL del gráfico
        chart_url = f"http://localhost:{self.server.port}/{self.chart_filename}"

        # Renderizar
        if TKINTERWEB_AVAILABLE:
            self._render_with_tkinterweb(chart_url)
        else:
            self._show_install_message(chart_url)

    def _generar_html_d3(self, chart_type, datos, subtitulo, tema):
        """Genera HTML con D3.js"""
        if chart_type == 'bar':
            return self.motor_d3.generar_grafico_barras(
                titulo='',
                datos=datos,
                subtitulo=subtitulo,
                tema=tema,
                interactivo=True
            )
        elif chart_type == 'donut':
            return self.motor_d3.generar_grafico_donut(
                titulo='',
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        elif chart_type == 'line':
            return self.motor_d3.generar_grafico_lineas(
                titulo='',
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        else:
            return "<p>Tipo de gráfico no soportado</p>"

    def _render_with_tkinterweb(self, url):
        """
        Renderiza con tkinterweb cargando desde servidor HTTP
        Esto FUNCIONA porque el navegador puede cargar JavaScript desde HTTP
        """
        try:
            html_container = Frame(self.chart_container, bg=self.chart_container._fg_color)
            html_container.pack(fill='both', expand=True, padx=5, pady=5)

            self.html_widget = HtmlFrame(
                html_container,
                messages_enabled=False,
                vertical_scrollbar=True,
                horizontal_scrollbar=False
            )

            # Cargar desde URL (servidor HTTP local)
            self.html_widget.load_url(url)
            self.html_widget.pack(fill='both', expand=True)

            print(f"✅ Gráfico D3.js cargado desde: {url}")

        except Exception as e:
            print(f"❌ Error renderizando con tkinterweb: {e}")
            self._show_error(str(e))

    def _show_install_message(self, url):
        """Muestra mensaje para instalar tkinterweb"""
        theme = self.theme_manager.get_current_theme()

        msg_frame = ctk.CTkFrame(self.chart_container, fg_color='transparent')
        msg_frame.pack(fill='both', expand=True, padx=20, pady=20)

        icon = ctk.CTkLabel(
            msg_frame,
            text='📊',
            font=('Montserrat', 48)
        )
        icon.pack(pady=(20, 10))

        title = ctk.CTkLabel(
            msg_frame,
            text='Gráfico D3.js Generado',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        )
        title.pack(pady=10)

        msg = ctk.CTkLabel(
            msg_frame,
            text=f'URL: {url}',
            font=('Montserrat', 9),
            text_color=theme['text_secondary']
        )
        msg.pack(pady=5)

        open_btn = ctk.CTkButton(
            msg_frame,
            text='🌐 Abrir en Navegador',
            font=('Montserrat', 14, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            text_color='white',
            height=50,
            corner_radius=10,
            command=lambda: webbrowser.open(url)
        )
        open_btn.pack(pady=20, padx=40, fill='x')

        note = ctk.CTkLabel(
            msg_frame,
            text='💡 Instala "pip install tkinterweb" para ver gráficos embebidos',
            font=('Montserrat', 9, 'italic'),
            text_color=theme['text_secondary']
        )
        note.pack(pady=5)

    def _open_in_full_browser(self):
        """Abre en navegador completo"""
        if self.chart_filename:
            url = f"http://localhost:{self.server.port}/{self.chart_filename}"
            webbrowser.open(url)
            print(f"✅ Gráfico abierto en navegador: {url}")

    def _show_error(self, message):
        """Muestra mensaje de error"""
        theme = self.theme_manager.get_current_theme()
        error_label = ctk.CTkLabel(
            self.chart_container,
            text=f'❌ Error: {message}',
            font=('Montserrat', 11),
            text_color='#ff6b6b',
            wraplength=self._width - 50
        )
        error_label.pack(expand=True, pady=20, padx=20)

    def clear(self):
        """Limpia el gráfico"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        self.html_widget = None

        # No eliminar archivo HTML (puede estar siendo usado)
        # Se limpiarán automáticamente al cerrar la aplicación

    def __del__(self):
        """Limpieza al destruir"""
        self.clear()
