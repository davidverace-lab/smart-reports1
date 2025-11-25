"""
Modal Fullscreen D3.js/NVD3.js - Gráficos Interactivos Embebidos con PyWebView
✨ CARACTERÍSTICAS:
- Ventana modal con gráficos D3.js/NVD3.js interactivos
- Embebido dentro de la aplicación usando PyWebView (motor nativo del sistema)
- Botón cerrar elegante (X) + tecla ESC
- Zoom, pan, tooltips, filtros interactivos
- Soporte para: bar, donut, line, area, horizontal_bar
- Motor dual: D3.js puro o NVD3.js (componentes reutilizables)
- Renderizado completo de JavaScript moderno (D3.js v7, NVD3.js v1.8.6)
"""
import customtkinter as ctk
from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.config.themes import HUTCHISON_COLORS
from smart_reports.utils.visualization.d3_generator import MotorTemplatesD3
from smart_reports.utils.visualization.nvd3_generator import MotorTemplatesNVD3
import os
import tempfile
import threading

try:
    import webview
    PYWEBVIEW_AVAILABLE = True
except ImportError:
    PYWEBVIEW_AVAILABLE = False
    print("⚠️ pywebview no disponible - Modal D3.js deshabilitado. Instala con: pip install pywebview")

# Alias para compatibilidad con código existente (deprecated)
TKINTERWEB_AVAILABLE = PYWEBVIEW_AVAILABLE


class ModalD3Fullscreen(ctk.CTkToplevel):
    """Modal fullscreen para mostrar gráficos D3.js/NVD3.js interactivos embebidos - CON INFORMACIÓN DE ORIGEN"""

    def __init__(self, parent, title, chart_type, chart_data, engine='nvd3', data_source=None, **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título del gráfico
            chart_type: Tipo de gráfico ('bar', 'donut', 'line', 'area')
            chart_data: Datos del gráfico {'labels': [...], 'values': [...]}
            engine: Motor de renderizado - 'nvd3' (default) o 'd3'
            data_source: Información del origen de datos (opcional)
        """
        super().__init__(parent, **kwargs)

        if not PYWEBVIEW_AVAILABLE:
            self.destroy()
            raise ImportError("pywebview no está instalado. Instala con: pip install pywebview")

        self.theme_manager = get_theme_manager()
        self.title_text = title
        self.chart_type = chart_type
        self.chart_data = chart_data
        self.engine = engine  # 'nvd3' o 'd3'
        self.data_source = data_source or self._get_default_data_source()

        # Referencias para pywebview
        self.webview_window = None
        self.webview_thread = None
        self.temp_file = None
        self._is_closing = False

        # Configurar ventana modal
        self._setup_window()
        self._create_ui()
        self._render_d3_chart()

        # Capturar tecla ESC
        self.bind('<Escape>', lambda e: self._close_modal())

        # Manejar cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self._close_modal)

    def _get_default_data_source(self):
        """Generar información por defecto del origen de datos"""
        from datetime import datetime
        return {
            'database': 'MySQL - Instituto Hutchison Ports',
            'table': 'instituto_progresomodulo',
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'records_count': len(self.chart_data.get('values', []))
        }

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
        self.main_container.pack(fill='both', expand=True, padx=20, pady=(20, 5))

        # === FOOTER CON INFORMACIÓN DE ORIGEN DE DATOS ===
        footer = ctk.CTkFrame(
            self,
            fg_color=theme['colors'].get('background_secondary', '#252525'),
            height=50,
            corner_radius=10
        )
        footer.pack(fill='x', side='bottom', padx=20, pady=(5, 20))
        footer.pack_propagate(False)

        # Información del origen de datos
        data_info_text = f"📊 Origen: {self.data_source['database']} | 📋 Tabla: {self.data_source['table']} | 🕐 Actualizado: {self.data_source['last_update']} | 📈 Registros: {self.data_source['records_count']}"

        info_label = ctk.CTkLabel(
            footer,
            text=data_info_text,
            font=("Montserrat", 11),
            text_color=theme['colors']['text_secondary']
        )
        info_label.pack(expand=True, pady=12)

    def _render_d3_chart(self):
        """Renderizar gráfico D3.js usando pywebview (motor nativo del navegador)"""
        try:
            print(f"  🔧 Generando HTML D3.js para tipo: {self.chart_type}")

            # Generar HTML con D3.js
            html_content = self._generate_d3_html()

            print(f"  ✅ HTML generado: {len(html_content)} caracteres")

            # Verificar que el HTML contiene elementos clave
            if 'd3.v7.min.js' not in html_content and 'nv.d3' not in html_content:
                raise ValueError("HTML no contiene referencia a D3.js/NVD3.js")

            if 'chart-container' not in html_content:
                raise ValueError("HTML no contiene chart-container")

            # Guardar HTML en archivo temporal
            self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
            self.temp_file.write(html_content)
            self.temp_file.close()

            print(f"  💾 HTML guardado en: {self.temp_file.name}")

            # Crear etiqueta de placeholder mientras carga webview
            loading_label = ctk.CTkLabel(
                self.main_container,
                text="🔄 Cargando gráfico interactivo D3.js...",
                font=("Montserrat", 14),
                text_color=self.theme_manager.get_current_theme()['colors']['text_secondary']
            )
            loading_label.pack(expand=True)

            # Iniciar pywebview en thread separado
            self.webview_thread = threading.Thread(target=self._start_webview, daemon=True)
            self.webview_thread.start()

            # Ocultar loading label después de un momento
            self.after(1000, lambda: loading_label.pack_forget() if loading_label.winfo_exists() else None)

            print("  ✅ Gráfico D3.js renderizado con PyWebView")

        except Exception as e:
            print(f"❌ Error renderizando D3.js: {e}")
            import traceback
            traceback.print_exc()

            # Mostrar mensaje de error detallado
            error_label = ctk.CTkLabel(
                self.main_container,
                text=f"⚠️ Error al cargar gráfico D3.js:\n{str(e)}\n\nVerifica:\n1. pywebview instalado (pip install pywebview>=4.0.0)\n2. Conexión a internet (para cargar D3.js desde CDN)\n3. Datos del gráfico válidos",
                font=("Montserrat", 12),
                text_color="red",
                justify="left"
            )
            error_label.pack(expand=True, padx=20, pady=20)

    def _start_webview(self):
        """Iniciar ventana pywebview (ejecuta en thread separado)"""
        try:
            # Calcular dimensiones y posición para el webview
            self.update_idletasks()

            # Obtener geometría del contenedor
            container_width = self.main_container.winfo_width()
            container_height = self.main_container.winfo_height()

            # Ajustar si las dimensiones son muy pequeñas (aún no renderizado)
            if container_width < 100:
                container_width = 1200
            if container_height < 100:
                container_height = 700

            print(f"  🌐 Creando ventana PyWebView ({container_width}x{container_height})...")

            # Crear ventana pywebview
            self.webview_window = webview.create_window(
                title=f"📊 {self.title_text}",
                url=self.temp_file.name,
                width=container_width,
                height=container_height,
                resizable=True,
                fullscreen=False,
                min_size=(800, 600),
                confirm_close=False
            )

            # Iniciar webview (bloquea hasta que se cierra la ventana)
            webview.start(debug=False)

            print("  ✅ Ventana PyWebView cerrada")

        except Exception as e:
            print(f"❌ Error iniciando PyWebView: {e}")
            import traceback
            traceback.print_exc()

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

    def _close_modal(self):
        """Cerrar modal y ventana pywebview"""
        if self._is_closing:
            return

        self._is_closing = True

        # Cerrar ventana pywebview si existe
        if self.webview_window:
            try:
                self.webview_window.destroy()
            except:
                pass

        # Destruir modal
        self._destroy_modal()

    def _destroy_modal(self):
        """Destruir modal y limpiar recursos"""
        # Limpiar archivo temporal si existe
        if self.temp_file:
            temp_path = self.temp_file.name if hasattr(self.temp_file, 'name') else self.temp_file
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                    print(f"  🗑️ Archivo temporal eliminado: {temp_path}")
                except Exception as e:
                    print(f"  ⚠️ No se pudo eliminar archivo temporal: {e}")

        self.destroy()


# ============================================================================
# FUNCIÓN DE CONVENIENCIA
# ============================================================================

def show_d3_chart(parent, title: str, chart_type: str, chart_data: dict, engine: str = 'nvd3', data_source: dict = None):
    """
    Mostrar gráfico D3.js/NVD3.js usando PyWebView (motor nativo del navegador) con información de origen de datos

    PyWebView utiliza el motor del navegador nativo del sistema (Edge/Chrome en Windows, Safari en macOS,
    WebKit en Linux), proporcionando soporte completo para JavaScript moderno (ES6+) y D3.js v7/NVD3.js v1.8.6.

    Args:
        parent: Widget padre (ventana principal)
        title: Título del gráfico
        chart_type: Tipo de gráfico ('bar', 'donut', 'line', 'area', 'horizontal_bar')
        chart_data: Datos del gráfico {'labels': [...], 'values': [...]}
        engine: Motor de renderizado - 'nvd3' (default) o 'd3'
        data_source: Información del origen de datos (opcional)
            Ejemplo: {
                'database': 'MySQL - Instituto Hutchison Ports',
                'table': 'instituto_progresomodulo',
                'last_update': '2024-01-15 10:30:00',
                'records_count': 150
            }

    Example:
        # Usando NVD3.js con información de origen
        show_d3_chart(
            parent=self.master,
            title="Ventas por Producto",
            chart_type="bar",
            chart_data={'labels': ['A', 'B', 'C'], 'values': [10, 20, 30]},
            engine='nvd3',
            data_source={
                'database': 'MySQL - Ventas',
                'table': 'ventas_productos',
                'last_update': '2024-01-15 10:30:00',
                'records_count': 3
            }
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
    if not PYWEBVIEW_AVAILABLE:
        print("⚠️ pywebview no está disponible - No se puede mostrar modal D3.js")
        print("   Instala con: pip install pywebview>=4.0.0")
        return

    modal = ModalD3Fullscreen(parent, title, chart_type, chart_data, engine=engine, data_source=data_source)
    modal.focus()
    # Nota: No usamos grab_set() porque pywebview crea su propia ventana independiente
