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
from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.config.themes import HUTCHISON_COLORS
from smart_reports.utils.visualization.d3_generator import MotorTemplatesD3
from smart_reports.ui.components.charts.chart_options_menu import ChartOptionsMenu

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
    Tarjeta con gráficos D3.js/NVD3.js - CON EXPANSIÓN IN-PLACE Y MENÚ DE OPCIONES

    Características:
    ✅ Usa D3.js/NVD3.js SIEMPRE (no Matplotlib)
    ✅ Expansión in-place (compacto ↔ expandido)
    ✅ Motor dual: D3.js puro o NVD3.js (componentes)
    ✅ Menú de opciones (⋮) con 7 funciones
    ✅ Actualizar datos con timestamp
    ✅ Si tkinterweb disponible → Embebido
    ✅ Si no disponible → Botón para navegador

    Flujo:
    1. Vista compacta con D3/NVD3 embebido
    2. Clic en ↗ → Expande in-place (regenera HTML más grande)
    3. Clic en ↙ → Colapsa a vista compacta
    4. Botón 🌐 → Abre en navegador en cualquier momento
    5. Botón ⋮ → Menú con opciones (ver tabla, exportar, stats, etc.)

    Parámetros:
        on_data_refresh: Callback opcional para actualizar datos (sin parámetros)
                        Se llama cuando el usuario hace clic en "Actualizar Datos"
    """

    def __init__(self, parent, title='', width=500, height=400, on_fullscreen=None,
                 on_data_refresh=None, engine='nvd3', **kwargs):
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(
            parent,
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            corner_radius=15,
            border_width=1,
            border_color=theme['colors']['border'],
            **kwargs
        )

        self._title = title
        self._width = width
        self._height = height
        self._compact_height = height  # Altura compacta original
        self._expanded_height = height * 2  # Altura expandida (2x)
        self.motor_d3 = MotorTemplatesD3()
        self.chart_engine = engine  # 'nvd3' (default) o 'd3'
        self.on_fullscreen = on_fullscreen  # Callback para modo fullscreen
        self.on_data_refresh = on_data_refresh  # Callback para actualizar datos

        # Estado
        self.chart_url = None
        self.chart_filepath = None
        self.html_content = None
        self.chart_type = None
        self.chart_data = None
        self.chart_subtitle = None
        self.is_expanded = False  # Estado de expansión

        # Referencias a widgets
        self.expand_btn = None  # Botón de expandir/colapsar
        self.title_label = None

        # Crear UI
        self._create_header()
        self._create_content_area()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _create_header(self):
        """Crear header del card"""
        if not self._title:
            return

        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(15, 10))

        # Título
        self.title_label = ctk.CTkLabel(
            header,
            text=self._title,
            font=('Montserrat', 16, 'bold'),
            text_color=theme['colors']['text'],
            anchor='w'
        )
        self.title_label.pack(side='left', fill='x', expand=True)

        # Controles (sin badges)
        controls_frame = ctk.CTkFrame(header, fg_color='transparent')
        controls_frame.pack(side='right')

        # Botón "Ver Grande" para expansión in-place
        self.expand_btn = ctk.CTkButton(
            controls_frame,
            text='⛶ Ver Grande',
            font=('Montserrat', 11, 'bold'),
            fg_color=HUTCHISON_COLORS['primary'],
            hover_color='#001a3d',
            text_color='white',
            corner_radius=6,
            width=110,
            height=28,
            command=self._toggle_expansion
        )
        self.expand_btn.pack(side='left', padx=5)

        # Menú de opciones (⋮)
        self.options_menu = ChartOptionsMenu(
            controls_frame,
            chart_title=self._title,
            chart_data=None,  # Se actualizará en set_chart
            chart_type=None,
            html_content=None,
            on_refresh=self.on_data_refresh  # Callback para actualizar datos
        )
        self.options_menu.pack(side='left', padx=5)

    def _create_content_area(self):
        """Crear área de contenido"""
        theme = self.theme_manager.get_current_theme()

        self.content_container = ctk.CTkFrame(
            self,
            fg_color=theme['colors']['background'] if self.theme_manager.is_dark_mode() else '#f8f9fa',
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

        # Actualizar menú de opciones con los datos actuales
        if hasattr(self, 'options_menu'):
            self.options_menu.chart_data = datos
            self.options_menu.chart_type = chart_type
            self.options_menu.html_content = self.html_content
            self.options_menu.chart_title = self._title

            # Actualizar timestamp de última actualización
            from datetime import datetime
            self.options_menu.last_update = datetime.now()

        print(f"✅ D3.js {chart_type}: {self.chart_url}")

    def _generate_d3_html(self, chart_type, datos, subtitulo, tema):
        """Generar HTML D3.js o NVD3.js según el motor configurado"""
        # Seleccionar motor de templates
        if self.chart_engine == 'nvd3':
            from smart_reports.utils.visualization.nvd3_generator import MotorTemplatesNVD3
            Motor = MotorTemplatesNVD3
        else:
            Motor = MotorTemplatesD3

        # Generar HTML según tipo
        if chart_type == 'bar':
            return Motor.generar_grafico_barras(
                titulo=self._title if not self.is_expanded else "",  # Sin título duplicado en expandido
                datos=datos,
                subtitulo=subtitulo,
                tema=tema,
                interactivo=True if self.chart_engine == 'd3' else None
            )
        elif chart_type == 'donut':
            return Motor.generar_grafico_donut(
                titulo=self._title if not self.is_expanded else "",
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        elif chart_type == 'line':
            return Motor.generar_grafico_lineas(
                titulo=self._title if not self.is_expanded else "",
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        elif chart_type == 'area':
            return Motor.generar_grafico_area(
                titulo=self._title if not self.is_expanded else "",
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
            text_color=theme['colors']['text']
        )
        title_label.pack(pady=(0, 8))

        # Descripción
        desc_label = ctk.CTkLabel(
            center_frame,
            text='Visualización interactiva con animaciones\ny funciones avanzadas de D3.js',
            font=('Montserrat', 11),
            text_color=theme['colors']['text_secondary'],
            justify='center'
        )
        desc_label.pack(pady=(0, 25))

        # Botón principal grande
        open_btn = ctk.CTkButton(
            center_frame,
            text='🚀 Abrir Gráfico Interactivo',
            font=('Montserrat', 14, 'bold'),
            fg_color=HUTCHISON_COLORS['primary'],
            hover_color=HUTCHISON_COLORS['primary'],
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
            text_color=theme['colors']['text_tertiary']
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

    def _toggle_expansion(self):
        """Toggle entre vista compacta y expandida"""
        if self.is_expanded:
            self._collapse_chart()
        else:
            self._expand_chart()

    def _expand_chart(self):
        """Expandir gráfico D3/NVD3 in-place (regenerar HTML con mayor tamaño)"""
        if not self.chart_type or not self.chart_data:
            return

        try:
            print(f"  📊 Expandiendo D3/NVD3: {self._title}")

            # Cambiar estado
            self.is_expanded = True

            # Actualizar botón
            self.expand_btn.configure(text="↙ Ver Pequeño")

            # Cambiar altura del contenedor
            self._height = self._expanded_height

            # Regenerar gráfico con nuevo tamaño
            self.set_chart(
                self.chart_type,
                self.chart_data,
                self.chart_subtitle or ''
            )

            print(f"  ✅ Expandido exitosamente")

        except Exception as e:
            print(f"❌ Error expandiendo: {e}")
            import traceback
            traceback.print_exc()
            self.is_expanded = False
            self.expand_btn.configure(text="⛶ Ver Grande")

    def _collapse_chart(self):
        """Colapsar gráfico D3/NVD3 in-place (regenerar HTML con tamaño compacto)"""
        try:
            print(f"  📉 Colapsando D3/NVD3: {self._title}")

            # Cambiar estado
            self.is_expanded = False

            # Actualizar botón
            self.expand_btn.configure(text="⛶ Ver Grande")

            # Cambiar altura del contenedor
            self._height = self._compact_height

            # Regenerar gráfico con tamaño compacto
            self.set_chart(
                self.chart_type,
                self.chart_data,
                self.chart_subtitle or ''
            )

            print(f"  ✅ Colapsado exitosamente")

        except Exception as e:
            print(f"❌ Error colapsando: {e}")
            import traceback
            traceback.print_exc()

    def clear(self):
        """Limpiar gráfico"""
        for widget in self.content_container.winfo_children():
            widget.destroy()

        self.chart_url = None
        self.html_content = None

    def _on_theme_changed(self, theme_mode: str):
        """Actualizar colores de la tarjeta cuando cambia el tema"""
        theme = self.theme_manager.get_current_theme()

        # Actualizar colores del frame principal
        self.configure(
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            border_color=theme['colors']['border']
        )

        # Actualizar título
        if self.title_label:
            self.title_label.configure(text_color=theme['colors']['text'])

        # Actualizar contenedor de contenido
        if hasattr(self, 'content_container'):
            self.content_container.configure(
                fg_color=theme['colors']['background'] if self.theme_manager.is_dark_mode() else '#f8f9fa'
            )

        # Regenerar el gráfico con el nuevo tema si hay datos
        if self.chart_type and self.chart_data:
            self.set_chart(self.chart_type, self.chart_data, self.chart_subtitle or '')
