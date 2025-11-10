"""
Componente D3ChartWebView - Gráficos D3.js REALMENTE interactivos
Usa PyWebView para ejecutar JavaScript dentro de la aplicación
"""
import customtkinter as ctk
from tkinter import Frame
import tempfile
import os
import threading
from config.themes import get_theme_manager
from config.themes import HUTCHISON_COLORS
from src.infrastructure.visualization.d3_generator import MotorTemplatesD3

# Intentar importar pywebview
try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("⚠️ PyWebView no está instalado. Instala con: pip install pywebview")


class D3ChartWebView(ctk.CTkFrame):
    """
    Tarjeta con gráficos D3.js TOTALMENTE interactivos
    Usa PyWebView (navegador embebido real) que SÍ ejecuta JavaScript
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
        self.webview_window = None
        self.current_html = None
        self.html_file = None

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

            # Badge D3.js
            badge = ctk.CTkLabel(
                header,
                text='D3.js ⚡',
                font=('Montserrat', 10, 'bold'),
                fg_color=HUTCHISON_COLORS['ports_sky_blue'],
                text_color='white',
                corner_radius=6,
                width=60,
                height=24
            )
            badge.pack(side='right', padx=5)

        # Container para el gráfico
        chart_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.chart_container = ctk.CTkFrame(self, fg_color=chart_bg, corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_d3_chart(self, chart_type, datos, subtitulo=''):
        """
        Establece gráfico D3.js interactivo embebido

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

        if WEBVIEW_AVAILABLE:
            self._render_with_webview(html)
        else:
            self._show_install_message()

    def _generar_html_d3(self, chart_type, datos, subtitulo, tema):
        """Genera HTML con D3.js interactivo"""
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

    def _render_with_webview(self, html):
        """
        Renderiza con PyWebView (navegador embebido REAL)
        Esto SÍ ejecuta JavaScript perfectamente
        """
        try:
            # Crear archivo temporal para el HTML
            if self.html_file is None:
                temp_file = tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix='.html',
                    delete=False,
                    encoding='utf-8'
                )
                temp_file.write(html)
                temp_file.close()
                self.html_file = temp_file.name
            else:
                # Actualizar archivo existente
                with open(self.html_file, 'w', encoding='utf-8') as f:
                    f.write(html)

            # Crear placeholder para webview
            placeholder = Frame(self.chart_container, bg=self.chart_container._fg_color)
            placeholder.pack(fill='both', expand=True, padx=5, pady=5)

            # Mensaje de carga
            loading_label = ctk.CTkLabel(
                placeholder,
                text="Cargando gráfico D3.js interactivo...",
                font=('Montserrat', 11),
                text_color='#a0a0b0'
            )
            loading_label.pack(expand=True)

            # Crear webview en thread separado
            def create_webview():
                try:
                    # Obtener el handle de la ventana de tkinter
                    window_handle = placeholder.winfo_id()

                    # Crear webview dentro del frame de tkinter
                    self.webview_window = webview.create_window(
                        '',  # Sin título (ya tenemos header)
                        f'file://{self.html_file}',
                        width=self._width - 30,
                        height=self._height - 100,
                        resizable=True,
                        frameless=True,  # Sin barra de título
                        easy_drag=False
                    )

                    # Iniciar webview
                    webview.start(debug=False, gui='edgechromium')  # Usar Edge en Windows

                    loading_label.configure(text="✅ Gráfico cargado")

                except Exception as e:
                    print(f"❌ Error creando webview: {e}")
                    loading_label.configure(
                        text=f"❌ Error: {e}\nInstala: pip install pywebview",
                        text_color='#ff6b6b'
                    )

            # Ejecutar en thread separado
            webview_thread = threading.Thread(target=create_webview, daemon=True)
            webview_thread.start()

            print("✅ Gráfico D3.js embebido con PyWebView")

        except Exception as e:
            print(f"❌ Error renderizando con webview: {e}")
            self._show_error(str(e))

    def _show_install_message(self):
        """Muestra mensaje para instalar pywebview"""
        theme = self.theme_manager.get_current_theme()

        msg_frame = ctk.CTkFrame(self.chart_container, fg_color='transparent')
        msg_frame.pack(fill='both', expand=True, padx=20, pady=20)

        icon = ctk.CTkLabel(
            msg_frame,
            text='⚠️',
            font=('Montserrat', 48)
        )
        icon.pack(pady=(20, 10))

        title = ctk.CTkLabel(
            msg_frame,
            text='PyWebView no está instalado',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        )
        title.pack(pady=10)

        msg = ctk.CTkLabel(
            msg_frame,
            text='Para gráficos D3.js interactivos embebidos,\ninstala PyWebView:',
            font=('Montserrat', 11),
            text_color=theme['text_secondary'],
            justify='center'
        )
        msg.pack(pady=10)

        cmd = ctk.CTkLabel(
            msg_frame,
            text='pip install pywebview',
            font=('Consolas', 12, 'bold'),
            fg_color='#2b2d42',
            text_color='#51cf66',
            corner_radius=8,
            padx=20,
            pady=10
        )
        cmd.pack(pady=15)

        note = ctk.CTkLabel(
            msg_frame,
            text='Después reinicia la aplicación',
            font=('Montserrat', 9, 'italic'),
            text_color=theme['text_secondary']
        )
        note.pack(pady=5)

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

        if self.webview_window:
            try:
                self.webview_window.destroy()
            except:
                pass
            self.webview_window = None

        if self.html_file and os.path.exists(self.html_file):
            try:
                os.unlink(self.html_file)
            except:
                pass
            self.html_file = None

    def __del__(self):
        """Limpieza al destruir el widget"""
        self.clear()
