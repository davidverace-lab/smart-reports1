"""
D3InteractiveChartCard - Gráfico D3.js/NVD3.js 100% Interactivo con Expansión In-Place
✨ CARACTERÍSTICAS PREMIUM:
- D3.js/NVD3.js desde el inicio (NO Matplotlib)
- Tooltips detallados con estadísticas automáticas
- Animación de "alzado" con hover effect (3D elevation)
- Click en elementos para ver data source (base de datos, tabla, etc.)
- ✅ Expansión IN-PLACE (↗/↙) - NO modal fullscreen
- ✅ Menú de opciones (⋮) con 7 funciones
- Servidor HTTP local para correcto renderizado JavaScript
- Funciona con tkinterweb (embedding) o navegador (fallback)
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
from smart_reports.utils.visualization.nvd3_generator_interactive import MotorTemplatesNVD3Interactive
from datetime import datetime

# Intentar importar tkinterweb para embedding
try:
    from tkinterweb import HtmlFrame
    TKINTERWEB_AVAILABLE = True
    print("✅ tkinterweb disponible - D3.js se mostrará embebido")
except Exception as e:
    TKINTERWEB_AVAILABLE = False
    print(f"⚠️ tkinterweb no disponible ({e}) - D3.js se abrirá en navegador")

# Ya no se usa modal fullscreen - ahora expansión in-place
# (Este código se mantiene comentado para referencia)
# try:
#     from smart_reports.ui.components.charts.modal_d3_fullscreen import ModalD3Fullscreen, PYWEBVIEW_AVAILABLE
# except ImportError:
#     PYWEBVIEW_AVAILABLE = False
#     ModalD3Fullscreen = None


# ============================================================================
# SERVIDOR HTTP GLOBAL SINGLETON
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

class D3InteractiveChartCard(ctk.CTkFrame):
    """
    Card con gráfico D3.js/NVD3.js 100% INTERACTIVO desde el inicio

    Características:
    - D3.js desde el inicio (no Matplotlib)
    - Tooltips automáticos con estadísticas
    - Hover effect con elevación 3D
    - Click para ver data source
    - Fullscreen con pywebview
    """

    def __init__(self, parent, title='', width=500, height=400, chart_engine='nvd3', data_source=None, **kwargs):
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
        self._expanded_height = height * 2.5  # Altura expandida (2.5x para mejor visualización)
        self.chart_engine = chart_engine  # 'nvd3' (default) o 'd3'
        self.motor_nvd3 = MotorTemplatesNVD3Interactive()

        # Data source para click handlers
        self.data_source = data_source or self._get_default_data_source()

        # Estado
        self.chart_url = None
        self.chart_filepath = None
        self.html_content = None
        self.chart_type = None
        self.chart_data = None
        self.chart_subtitle = None
        self.is_expanded = False  # Estado de expansión

        # Referencias a widgets
        self.expand_btn = None
        self.options_menu = None
        self.data_table_widget = None  # Widget de tabla expandible
        self.table_visible = False  # Estado de visibilidad de tabla

        # Crear UI
        self._create_header()
        self._create_content_area()

    def _get_default_data_source(self):
        """Data source por defecto"""
        return {
            'database': 'MySQL - Instituto Hutchison Ports',
            'table': 'Data Visualization',
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'records_count': 0
        }

    def _create_header(self):
        """Crear header del card RESPONSIVE"""
        if not self._title:
            return

        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=15, pady=(15, 10))
        header.grid_columnconfigure(0, weight=1)  # El título se expande
        header.grid_columnconfigure(1, weight=0)  # Los controles NO se expanden

        # Título
        title_label = ctk.CTkLabel(
            header,
            text=self._title,
            font=('Montserrat', 14, 'bold'),
            text_color=theme['colors']['text'],
            anchor='w'
        )
        title_label.grid(row=0, column=0, sticky='w', padx=(5, 10))

        # Controles (botones en fila)
        controls_frame = ctk.CTkFrame(header, fg_color='transparent')
        controls_frame.grid(row=0, column=1, sticky='e')

        # Botón "Ver Grande" para expansión in-place - MÁS VISIBLE
        self.expand_btn = ctk.CTkButton(
            controls_frame,
            text='⛶',  # Icono de expandir
            font=('Segoe UI', 16, 'bold'),  # Fuente más grande y legible
            fg_color=HUTCHISON_COLORS['primary'],
            hover_color='#001a3d',
            text_color='white',
            corner_radius=8,
            width=40,  # Más ancho
            height=32,  # Más alto
            command=self._toggle_expansion
        )
        self.expand_btn.pack(side='left', padx=(0, 5))

        # Menú de opciones (⋮)
        from smart_reports.ui.components.charts.chart_options_menu import ChartOptionsMenu

        self.options_menu = ChartOptionsMenu(
            controls_frame,
            chart_title=self._title,
            chart_data=None,  # Se actualizará en set_chart
            chart_type=None,
            html_content=None,
            on_refresh=None,  # Callback opcional para actualizar datos
            on_show_table=self._toggle_data_table  # Callback para mostrar tabla
        )
        self.options_menu.pack(side='left')

    def _create_content_area(self):
        """Crear área de contenido"""
        theme = self.theme_manager.get_current_theme()

        self.content_container = ctk.CTkFrame(
            self,
            fg_color=theme['colors']['background'] if self.theme_manager.is_dark_mode() else '#f8f9fa',
            corner_radius=10
        )
        self.content_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_chart(self, chart_type, datos, subtitulo='', data_source=None):
        """
        Establecer gráfico D3.js/NVD3.js INTERACTIVO

        Args:
            chart_type: 'bar', 'donut', 'line', 'area', etc.
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Subtítulo opcional
            data_source: Dict con info de origen de datos (opcional)
        """
        print(f"\n📊 [D3InteractiveChartCard] set_chart() llamado")
        print(f"  🔹 Título: {self._title}")
        print(f"  🔹 Tipo: {chart_type}")
        print(f"  🔹 Datos: {datos}")
        print(f"  🔹 Subtítulo: {subtitulo}")

        # Actualizar data source si se proporciona
        if data_source:
            self.data_source = data_source
        else:
            # Actualizar records_count con datos reales
            self.data_source['records_count'] = len(datos.get('labels', []))
            self.data_source['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Guardar datos del chart
        self.chart_type = chart_type
        self.chart_data = datos
        self.chart_subtitle = subtitulo

        # Limpiar contenido anterior
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Generar HTML D3.js INTERACTIVO
        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'
        print(f"  🔹 Tema: {tema}")

        self.html_content = self._generate_d3_interactive_html(chart_type, datos, subtitulo, tema)

        print(f"  🔹 HTML generado: {len(self.html_content)} caracteres")

        # Guardar y obtener URL
        chart_id = f"{id(self)}_{chart_type}"
        self.chart_url, self.chart_filepath = _D3_SERVER.save_chart(
            self.html_content,
            chart_id
        )

        print(f"  🔹 Archivo guardado: {self.chart_filepath}")
        print(f"  🔹 URL: {self.chart_url}")

        # Renderizar SIEMPRE embebido (con fallback si falla)
        self._render_embedded()

        # Actualizar menú de opciones con los datos actuales
        if hasattr(self, 'options_menu') and self.options_menu:
            self.options_menu.chart_data = datos
            self.options_menu.chart_type = chart_type
            self.options_menu.html_content = self.html_content
            self.options_menu.chart_title = self._title

            # Actualizar timestamp de última actualización
            self.options_menu.last_update = datetime.now()

        print(f"✅ D3.js Interactivo {chart_type}: {self.chart_url}")

    def _generate_d3_interactive_html(self, chart_type, datos, subtitulo, tema):
        """Generar HTML D3.js INTERACTIVO según el tipo"""
        if chart_type == 'bar' or chart_type == 'horizontal_bar':
            return self.motor_nvd3.generar_grafico_barras_interactivo(
                titulo=self._title,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema,
                data_source=self.data_source,
                chart_height=int(self._height)
            )
        elif chart_type == 'donut' or chart_type == 'pie':
            return self.motor_nvd3.generar_grafico_donut_interactivo(
                titulo=self._title,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema,
                data_source=self.data_source,
                chart_height=int(self._height)
            )
        elif chart_type == 'line':
            return self.motor_nvd3.generar_grafico_lineas_interactivo(
                titulo=self._title,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema,
                data_source=self.data_source,
                chart_height=int(self._height)
            )
        else:
            # Fallback a barras
            return self.motor_nvd3.generar_grafico_barras_interactivo(
                titulo=self._title,
                datos=datos,
                subtitulo=subtitulo,
                tema=tema,
                data_source=self.data_source,
                chart_height=int(self._height)
            )

    def _render_embedded(self):
        """Renderizar embebido con tkinterweb"""
        try:
            print(f"  🔍 [DEBUG] Intentando renderizar embebido...")
            print(f"  🔍 [DEBUG] Chart URL: {self.chart_url}")
            print(f"  🔍 [DEBUG] Chart File: {self.chart_filepath}")
            print(f"  🔍 [DEBUG] TKINTERWEB_AVAILABLE: {TKINTERWEB_AVAILABLE}")

            if not TKINTERWEB_AVAILABLE:
                print(f"  ⚠️ tkinterweb no disponible, usando vista de botón")
                self._render_button_view()
                return

            # Verificar que el archivo HTML existe
            if not os.path.exists(self.chart_filepath):
                print(f"  ❌ ERROR: Archivo HTML no existe: {self.chart_filepath}")
                self._render_button_view()
                return

            print(f"  ✅ Archivo HTML existe ({os.path.getsize(self.chart_filepath)} bytes)")

            html_frame = Frame(
                self.content_container,
                bg=self.content_container._fg_color
            )
            html_frame.pack(fill='both', expand=True, padx=5, pady=5)

            print(f"  ✅ Frame creado")

            # HtmlFrame SIN SCROLLBARS (clean UI)
            html_widget = HtmlFrame(
                html_frame,
                messages_enabled=False,
                vertical_scrollbar=False,  # Sin scrollbar vertical
                horizontal_scrollbar=False  # Sin scrollbar horizontal
            )

            print(f"  ✅ HtmlFrame creado")

            # IMPORTANTE: Cargar desde URL HTTP (ejecuta JavaScript correctamente)
            html_widget.load_url(self.chart_url)
            html_widget.pack(fill='both', expand=True)

            print(f"  ✅ D3.js Interactivo renderizado embebido en: {self.chart_url}")

        except Exception as e:
            import traceback
            print(f"  ❌ Error embebiendo: {e}")
            print(f"  ❌ Traceback: {traceback.format_exc()}")
            # Fallback a vista de botón
            for widget in self.content_container.winfo_children():
                widget.destroy()
            self._render_button_view()

    def _render_button_view(self):
        """Renderizar vista con botón para abrir (fallback)"""
        theme = self.theme_manager.get_current_theme()

        center_frame = ctk.CTkFrame(self.content_container, fg_color='transparent')
        center_frame.pack(expand=True)

        # Icono
        icon_label = ctk.CTkLabel(
            center_frame,
            text='📊✨',
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
            text='Con tooltips avanzados, hover effects 3D\ny click para ver origen de datos',
            font=('Montserrat', 11),
            text_color=theme['colors']['text_secondary'],
            justify='center'
        )
        desc_label.pack(pady=(0, 25))

        # Botón principal
        open_btn = ctk.CTkButton(
            center_frame,
            text='🚀 Abrir Gráfico Interactivo',
            font=('Montserrat', 14, 'bold'),
            fg_color=HUTCHISON_COLORS['primary'],
            hover_color='#001a3d',
            text_color='white',
            corner_radius=12,
            height=50,
            width=280,
            command=self._open_in_browser
        )
        open_btn.pack(pady=(0, 10))

        # Nota
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
            print("⚠️ No hay URL de gráfico para abrir")
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
            print(f"  📊 Expandiendo D3/NVD3 Interactivo: {self._title}")

            # Cambiar estado
            self.is_expanded = True

            # Actualizar botón (cambiar ícono)
            self.expand_btn.configure(text="↙")

            # Cambiar altura del contenedor (2.5x el tamaño original)
            self._height = self._expanded_height

            # Configurar altura mínima del contenedor (para que se expanda visualmente)
            self.configure(height=int(self._height) + 150)  # +150 para header y padding

            # Regenerar gráfico con nuevo tamaño
            self.set_chart(
                self.chart_type,
                self.chart_data,
                self.chart_subtitle or ''
            )

            print(f"  ✅ Expandido exitosamente a {self._height}px")

        except Exception as e:
            print(f"❌ Error expandiendo: {e}")
            import traceback
            traceback.print_exc()
            self.is_expanded = False
            self.expand_btn.configure(text="⛶")

    def _collapse_chart(self):
        """Colapsar gráfico D3/NVD3 in-place (regenerar HTML con tamaño compacto)"""
        try:
            print(f"  📉 Colapsando D3/NVD3 Interactivo: {self._title}")

            # Cambiar estado
            self.is_expanded = False

            # Actualizar botón (restaurar ícono)
            self.expand_btn.configure(text="⛶")

            # Cambiar altura del contenedor
            self._height = self._compact_height

            # Restaurar altura original del contenedor
            self.configure(height=int(self._height) + 150)  # +150 para header y padding

            # Regenerar gráfico con tamaño compacto
            self.set_chart(
                self.chart_type,
                self.chart_data,
                self.chart_subtitle or ''
            )

            print(f"  ✅ Colapsado exitosamente a {self._height}px")

        except Exception as e:
            print(f"❌ Error colapsando: {e}")
            import traceback
            traceback.print_exc()

    def _toggle_data_table(self):
        """Mostrar/ocultar tabla de datos expandible IN-PLACE"""
        if self.table_visible:
            self._hide_data_table()
        else:
            self._show_data_table()

    def _show_data_table(self):
        """Mostrar tabla de datos expandible"""
        if not self.chart_data or 'labels' not in self.chart_data:
            print("⚠️ No hay datos para mostrar en la tabla")
            return

        try:
            print(f"📊 Mostrando tabla de datos para: {self._title}")

            # Ocultar gráfico
            self.content_container.pack_forget()

            # Crear widget de tabla expandible
            from smart_reports.ui.components.charts.data_table_expandable import DataTableExpandable

            self.data_table_widget = DataTableExpandable(
                self,
                title=self._title,
                data=self.chart_data,
                chart_type=self.chart_type,
                on_close=self._hide_data_table
            )
            self.data_table_widget.pack(fill='both', expand=True, padx=15, pady=(0, 15))

            self.table_visible = True
            print("✅ Tabla de datos mostrada")

        except Exception as e:
            print(f"❌ Error mostrando tabla: {e}")
            import traceback
            traceback.print_exc()

    def _hide_data_table(self):
        """Ocultar tabla de datos y restaurar gráfico"""
        try:
            print(f"📊 Ocultando tabla de datos para: {self._title}")

            # Destruir tabla
            if self.data_table_widget:
                self.data_table_widget.destroy()
                self.data_table_widget = None

            # Restaurar gráfico
            self.content_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

            self.table_visible = False
            print("✅ Tabla de datos ocultada")

        except Exception as e:
            print(f"❌ Error ocultando tabla: {e}")
            import traceback
            traceback.print_exc()

    def clear(self):
        """Limpiar gráfico"""
        for widget in self.content_container.winfo_children():
            widget.destroy()

        self.chart_url = None
        self.html_content = None
        self.chart_type = None
        self.chart_data = None
