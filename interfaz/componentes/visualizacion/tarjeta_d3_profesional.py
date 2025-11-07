"""
Componente ProfessionalD3ChartCard - SOLUCIÓN DEFINITIVA
Gráficos matplotlib embebidos nativamente que SIEMPRE funcionan
"""
import customtkinter as ctk
from tkinter import Frame
import tempfile
import webbrowser
from nucleo.configuracion.gestor_temas import get_theme_manager
from nucleo.configuracion.ajustes import HUTCHISON_COLORS
from nucleo.servicios.motor_templates_d3 import MotorTemplatesD3
from nucleo.servicios.motor_graficos_matplotlib import MotorGraficosMatplotlib


class ProfessionalD3ChartCard(ctk.CTkFrame):
    """Card con gráficos matplotlib embebidos nativamente - SOLUCIÓN DEFINITIVA"""

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
        self.canvas_widget = None
        self.current_html_d3 = None
        self.current_chart_type = None
        self.current_datos = None

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

            # Badge Matplotlib
            badge = ctk.CTkLabel(
                btn_frame,
                text='📊',
                font=('Montserrat', 14, 'bold'),
                fg_color=HUTCHISON_COLORS['ports_sky_blue'],
                text_color='white',
                corner_radius=6,
                width=35,
                height=24
            )
            badge.pack(side='left', padx=5)

            # Botón D3.js interactivo (abre en navegador)
            self.d3_btn = ctk.CTkButton(
                btn_frame,
                text='D3',
                font=('Montserrat', 10, 'bold'),
                fg_color=HUTCHISON_COLORS['success'],
                hover_color='#41a755',
                text_color='white',
                corner_radius=6,
                width=35,
                height=28,
                command=self._open_d3_in_browser
            )
            self.d3_btn.pack(side='left', padx=5)

        # Container para el gráfico
        chart_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.chart_container = ctk.CTkFrame(self, fg_color=chart_bg, corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_d3_chart(self, chart_type, datos, subtitulo=''):
        """
        Establecer gráfico (matplotlib embebido + D3.js para navegador)

        Args:
            chart_type: Tipo de gráfico ('bar', 'donut', 'line')
            datos: Diccionario con datos del gráfico
            subtitulo: Subtítulo del gráfico (no usado en matplotlib)
        """
        # Guardar datos para regenerar
        self.current_chart_type = chart_type
        self.current_datos = datos

        # Limpiar contenido anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        self.canvas_widget = None

        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'

        # 1. Generar HTML D3.js para navegador (siempre disponible)
        self.current_html_d3 = self._generar_html_d3(chart_type, datos, subtitulo, tema)

        # 2. Renderizar gráfico matplotlib embebido (SIEMPRE FUNCIONA)
        try:
            self._render_matplotlib(chart_type, datos, tema)
            print(f"✅ Gráfico {chart_type} renderizado con matplotlib")
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

    def _open_d3_in_browser(self):
        """Abrir versión D3.js interactiva en navegador"""
        if not self.current_html_d3:
            return

        try:
            # Guardar HTML en archivo temporal
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
            print(f"✅ Gráfico D3.js interactivo abierto en navegador")
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
        self.canvas_widget = None
        self.current_html_d3 = None
        self.current_chart_type = None
        self.current_datos = None
