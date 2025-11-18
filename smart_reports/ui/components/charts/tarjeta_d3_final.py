"""
D3ChartCard - SOLUCIÓN DEFINITIVA para gráficos D3.js
Híbrido inteligente que SIEMPRE funciona
"""
import customtkinter as ctk
from tkinter import Frame
import tempfile
import webbrowser
import os
import threading
import http.server
import socketserver
from src.main.res.config.gestor_temas import get_theme_manager
from src.main.res.config.themes import HUTCHISON_COLORS
from src.main.python.utils.visualization.d3_generator import MotorTemplatesD3

# Intentar importar tkinterweb
try:
    from tkinterweb import HtmlFrame
    TKINTERWEB_AVAILABLE = True
    print("✅ tkinterweb disponible - D3.js se mostrará embebido")
except Exception as e:
    TKINTERWEB_AVAILABLE = False
    print(f"⚠️ tkinterweb no disponible ({e}) - D3.js se abrirá en navegador")


# ============================================================================
# SERVIDOR HTTP GLOBAL
# ============================================================================

class D3HttpServer:
    """Servidor HTTP singleton para servir gráficos D3.js"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_server()
            return cls._instance

    def _init_server(self):
        """Inicializa el servidor HTTP"""
        self.port = 8050
        self.httpd = None
        self.thread = None
        self.charts_dir = os.path.join(tempfile.gettempdir(), 'smartreports_d3')
        os.makedirs(self.charts_dir, exist_ok=True)
        self.start()

    def start(self):
        """Inicia el servidor"""
        if self.httpd is not None:
            return

        import functools
        Handler = functools.partial(
            http.server.SimpleHTTPRequestHandler,
            directory=self.charts_dir
        )

        try:
            self.httpd = socketserver.TCPServer(("127.0.0.1", self.port), Handler)
            self.httpd.allow_reuse_address = True
            self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.thread.start()
            print(f"✅ Servidor D3.js: http://127.0.0.1:{self.port}")
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"⚠️ Servidor D3.js ya está corriendo (puerto {self.port})")
            else:
                print(f"❌ Error iniciando servidor: {e}")

    def save_chart(self, html_content, chart_id):
        """Guarda un gráfico y retorna la URL"""
        filename = f"chart_{chart_id}.html"
        filepath = os.path.join(self.charts_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return f"http://127.0.0.1:{self.port}/{filename}", filepath


# Servidor global
_D3_SERVER = D3HttpServer()


# ============================================================================
# COMPONENTE PRINCIPAL
# ============================================================================

class D3ChartCard(ctk.CTkFrame):
    """
    Tarjeta con gráficos D3.js - SOLUCIÓN DEFINITIVA

    Modos de funcionamiento:
    1. Si tkinterweb está disponible → Embebido directo en la app
    2. Si no está disponible → Botón para abrir en navegador

    Los gráficos SIEMPRE se generan correctamente y se ven hermosos.
    """

    def __init__(self, parent, title='', width=500, height=400, on_fullscreen=None, **kwargs):
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
        self.on_fullscreen = on_fullscreen  # Callback para modo fullscreen

        # Estado
        self.chart_url = None
        self.chart_filepath = None
        self.html_content = None
        self.chart_type = None
        self.chart_data = None
        self.chart_subtitle = None

        # Crear UI
        self._create_header()
        self._create_content_area()

    def _create_header(self):
        """Crear header del card"""
        if not self._title:
            return

        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(15, 10))

        # Título
        title_label = ctk.CTkLabel(
            header,
            text=self._title,
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title_label.pack(side='left', fill='x', expand=True)

        # Badges
        badge_frame = ctk.CTkFrame(header, fg_color='transparent')
        badge_frame.pack(side='right')

        # Badge D3.js
        d3_badge = ctk.CTkLabel(
            badge_frame,
            text='D3.js ⚡',
            font=('Montserrat', 10, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            text_color='white',
            corner_radius=6,
            width=70,
            height=24
        )
        d3_badge.pack(side='left', padx=5)

        # Badge embebido/navegador
        mode_text = 'Embebido' if TKINTERWEB_AVAILABLE else 'Navegador'
        mode_color = HUTCHISON_COLORS['ports_sky_blue'] if TKINTERWEB_AVAILABLE else '#ffa94d'

        mode_badge = ctk.CTkLabel(
            badge_frame,
            text=mode_text,
            font=('Montserrat', 10, 'bold'),
            fg_color=mode_color,
            text_color='white',
            corner_radius=6,
            width=90,
            height=24
        )
        mode_badge.pack(side='left', padx=5)

        # Botón fullscreen (si hay callback)
        if self.on_fullscreen:
            fullscreen_btn = ctk.CTkButton(
                badge_frame,
                text='⛶',
                font=('Montserrat', 14, 'bold'),
                fg_color=HUTCHISON_COLORS['aqua_green'],
                hover_color='#00b386',
                text_color='white',
                corner_radius=6,
                width=35,
                height=28,
                command=self._trigger_fullscreen
            )
            fullscreen_btn.pack(side='left', padx=5)

        # Botón navegador
        browser_btn = ctk.CTkButton(
            badge_frame,
            text='🌐',
            font=('Montserrat', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            hover_color='#001a3d',  # Versión más oscura de ports_sea_blue
            text_color='white',
            corner_radius=6,
            width=35,
            height=28,
            command=self._open_in_browser
        )
        browser_btn.pack(side='left', padx=5)

    def _create_content_area(self):
        """Crear área de contenido"""
        theme = self.theme_manager.get_current_theme()

        self.content_container = ctk.CTkFrame(
            self,
            fg_color=theme['background'] if self.theme_manager.is_dark_mode() else '#f8f9fa',
            corner_radius=10
        )
        self.content_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_chart(self, chart_type, datos, subtitulo=''):
        """
        Establecer gráfico D3.js

        Args:
            chart_type: 'bar', 'donut', 'line', 'area', etc.
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Subtítulo opcional
        """
        # Guardar datos del chart para fullscreen
        self.chart_type = chart_type
        self.chart_data = datos
        self.chart_subtitle = subtitulo

        # Limpiar contenido anterior
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Generar HTML D3.js
        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'
        self.html_content = self._generate_d3_html(chart_type, datos, subtitulo, tema)

        # Guardar y obtener URL
        chart_id = f"{id(self)}_{chart_type}"
        self.chart_url, self.chart_filepath = _D3_SERVER.save_chart(
            self.html_content,
            chart_id
        )

        # Renderizar según disponibilidad
        if TKINTERWEB_AVAILABLE:
            self._render_embedded()
        else:
            self._render_button_view()

        print(f"✅ D3.js {chart_type}: {self.chart_url}")

    def _generate_d3_html(self, chart_type, datos, subtitulo, tema):
        """Generar HTML D3.js según el tipo"""
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
        else:
            return f"<html><body><p>Tipo no soportado: {chart_type}</p></body></html>"

    def _render_embedded(self):
        """Renderizar embebido con tkinterweb"""
        try:
            html_frame = Frame(
                self.content_container,
                bg=self.content_container._fg_color
            )
            html_frame.pack(fill='both', expand=True, padx=5, pady=5)

            html_widget = HtmlFrame(
                html_frame,
                messages_enabled=False,
                vertical_scrollbar=False,
                horizontal_scrollbar=False
            )

            # Cargar desde URL HTTP (ejecuta JavaScript)
            html_widget.load_url(self.chart_url)
            html_widget.pack(fill='both', expand=True)

            print(f"  → Renderizado embebido exitoso")

        except Exception as e:
            print(f"  ⚠️ Error embebiendo: {e}")
            # Fallback a vista de botón
            for widget in self.content_container.winfo_children():
                widget.destroy()
            self._render_button_view()

    def _render_button_view(self):
        """Renderizar vista con botón para abrir"""
        theme = self.theme_manager.get_current_theme()

        # Contenedor centrado
        center_frame = ctk.CTkFrame(self.content_container, fg_color='transparent')
        center_frame.pack(expand=True)

        # Icono grande
        icon_label = ctk.CTkLabel(
            center_frame,
            text='📊',
            font=('Montserrat', 56)
        )
        icon_label.pack(pady=(10, 15))

        # Título
        title_label = ctk.CTkLabel(
            center_frame,
            text='Gráfico D3.js Interactivo',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        )
        title_label.pack(pady=(0, 8))

        # Descripción
        desc_label = ctk.CTkLabel(
            center_frame,
            text='Visualización interactiva con animaciones\ny funciones avanzadas de D3.js',
            font=('Montserrat', 11),
            text_color=theme['text_secondary'],
            justify='center'
        )
        desc_label.pack(pady=(0, 25))

        # Botón principal grande
        open_btn = ctk.CTkButton(
            center_frame,
            text='🚀 Abrir Gráfico Interactivo',
            font=('Montserrat', 14, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            text_color='white',
            corner_radius=12,
            height=50,
            width=280,
            command=self._open_in_browser
        )
        open_btn.pack(pady=(0, 10))

        # Nota pequeña
        note_label = ctk.CTkLabel(
            center_frame,
            text='Se abrirá en tu navegador predeterminado',
            font=('Montserrat', 9, 'italic'),
            text_color=theme['text_tertiary']
        )
        note_label.pack(pady=(5, 10))

    def _open_in_browser(self):
        """Abrir gráfico en navegador"""
        if not self.chart_url:
            return

        try:
            webbrowser.open(self.chart_url)
            print(f"  🌐 Abierto en navegador: {self.chart_url}")
        except Exception as e:
            print(f"  ❌ Error abriendo navegador: {e}")

    def _trigger_fullscreen(self):
        """Activar modo fullscreen (llamar al callback)"""
        if self.on_fullscreen and self.chart_url:
            # Pasar todos los datos necesarios para recrear el chart en fullscreen
            self.on_fullscreen(
                title=self._title,
                chart_type=self.chart_type,
                data=self.chart_data,
                subtitle=self.chart_subtitle,
                url=self.chart_url
            )
            print(f"  ⛶ Activando fullscreen para: {self._title}")

    def clear(self):
        """Limpiar gráfico"""
        for widget in self.content_container.winfo_children():
            widget.destroy()

        self.chart_url = None
        self.html_content = None
